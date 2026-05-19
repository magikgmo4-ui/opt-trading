# ShareX quick setup (SFTP) -> vision_bot inbox

## Goal
Each capture is uploaded to:
`/srv/sftp/shared_files/shared/vision_inbox`

## Steps (ShareX)
1) Destinations -> Destination settings...
2) Custom uploaders -> New -> SFTP
3) Host: (admin-trading IP)
   Port: 22
   Username: (ton user SFTP, ex: ghost)
   Auth: Private key (recommandé)
   Remote directory: /srv/sftp/shared_files/shared/vision_inbox
4) File name pattern (suggestion):
   {yyyy}-{MM}-{dd}_{HH}-{mm}-{ss}_{rn:6}.png

## Outputs
vision_bot writes:
- .md and .txt into: `/srv/sftp/shared_files/shared/vision_outbox`
- processed images into: `/srv/sftp/shared_files/shared/vision_processed`
