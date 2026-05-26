import os
import time
import yaml
import requests
from typing import Dict, Any, Optional, List

class GitHubActionsBridge:
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo = os.getenv("GITHUB_REPOSITORY")  # format: "owner/repo"
        self.api_base = "https://api.github.com"
        
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        if not self.repo:
            raise ValueError("GITHUB_REPOSITORY environment variable not set")

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def load_registry(self) -> Dict[str, Any]:
        with open(self.registry_path, 'r') as f:
            return yaml.safe_load(f)

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        registry = self.load_registry()
        for job in registry.get("jobs", []):
            if job["job_id"] == job_id:
                return job
        return None

    def trigger_workflow(self, job_id: str, inputs: Optional[Dict[str, Any]] = None, ref: str = "sot/mainline") -> Dict[str, Any]:
        job = self.get_job(job_id)
        if not job:
            return {"ok": False, "error": f"Job {job_id} not found in registry"}
        
        if not job.get("orchestrable_by_openclaw", False):
            return {"ok": False, "error": f"Job {job_id} is not orchestrable by OpenClaw"}
        
        workflow_path = job.get("workflow")
        if not workflow_path:
            return {"ok": False, "error": f"Job {job_id} has no workflow file associated"}
        
        # GitHub API uses filename, not full path
        workflow_filename = os.path.basename(workflow_path)
        
        url = f"{self.api_base}/repos/{self.repo}/actions/workflows/{workflow_filename}/dispatches"
        data = {
            "ref": ref,
            "inputs": inputs or {}
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        
        if response.status_code == 204:
            return {"ok": True, "message": f"Workflow {workflow_filename} triggered for job {job_id}"}
        else:
            return {"ok": False, "error": f"Failed to trigger workflow: {response.text}", "status_code": response.status_code}

    def get_latest_run(self, workflow_filename: str) -> Optional[Dict[str, Any]]:
        url = f"{self.api_base}/repos/{self.repo}/actions/workflows/{workflow_filename}/runs"
        response = requests.get(url, headers=self._get_headers(), params={"per_page": 1})
        if response.status_code == 200:
            runs = response.json().get("workflow_runs", [])
            return runs[0] if runs else None
        return None

    def poll_run_status(self, run_id: int, timeout_s: int = 600, interval_s: int = 30) -> Dict[str, Any]:
        start_time = time.time()
        url = f"{self.api_base}/repos/{self.repo}/actions/runs/{run_id}"
        
        while time.time() - start_time < timeout_s:
            response = requests.get(url, headers=self._get_headers())
            if response.status_code == 200:
                run_data = response.json()
                status = run_data.get("status")
                conclusion = run_data.get("conclusion")
                
                if status == "completed":
                    return {
                        "ok": True,
                        "status": status,
                        "conclusion": conclusion,
                        "run_id": run_id,
                        "html_url": run_data.get("html_url"),
                        "workflow_id": run_data.get("workflow_id")
                    }
                
                print(f"Run {run_id} status: {status}...")
            else:
                return {"ok": False, "error": f"Failed to poll run status: {response.text}"}
            
            time.sleep(interval_s)
            
        return {"ok": False, "error": "Timeout reached while polling run status"}

    def get_run_jobs(self, run_id: int) -> Dict[str, Any]:
        url = f"{self.api_base}/repos/{self.repo}/actions/runs/{run_id}/jobs"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return {"ok": True, "jobs": response.json().get("jobs", [])}
        else:
            return {"ok": False, "error": f"Failed to get jobs for run {run_id}: {response.text}"}

    def get_job_logs(self, job_id: int) -> Dict[str, Any]:
        url = f"{self.api_base}/repos/{self.repo}/actions/jobs/{job_id}/logs"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return {"ok": True, "content": response.text}
        else:
            return {"ok": False, "error": f"Failed to get logs for job {job_id}: {response.text}"}

if __name__ == "__main__":
    # Minimal self-test if run as script
    try:
        bridge = GitHubActionsBridge("docs/registries/GITHUB_ACTIONS_JOBS_REGISTRY_01.yml")
        print("Bridge initialized (token found)")
    except Exception as e:
        print(f"Initialization skipped: {e}")
