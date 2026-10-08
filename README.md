# Crew Lopez Surfhouse

The Django website has four main menu items: Home, Activities, Villa (house and rooms), and About. Booking opens the configured external listing. Contact, the blog archive and policies live in the footer.

## Run the editable site

```bash
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

Open http://127.0.0.1:8000 and manage content at http://127.0.0.1:8000/admin/.

In admin:

- **Photos:** one gallery for page images, artwork, room photos and activity
  photos. Each card shows the current picture and updates the original record.
  Drop a replacement or choose a file, drag/zoom the crop, and select Save photo.
  Desktop and Mobile controls measure frames from the live page layouts at
  1440px and 390px. Shared images use the first matching location on their page;
  other responsive sizes keep the site's existing CSS layout and object-fit.
  The gallery respects each original model's change permissions. Registered
  content models with file fields are included automatically. This project has
  no team-member model or article image fields yet.

- **Site settings:** homepage title, description and photo; brand illustration; booking link; business and contact details; editable policies and owner approval status.
- **Rooms:** names, descriptions, photos and ordering. All rooms appear on the site.
- **Activities:** names, descriptions, photos, symbols and ordering. All activities appear on the site.
- **Blog posts:** archive stories, categories, publication status and ordering.
- **Site images:** replace the bundled villa photos, room illustrations, activity
  fallback photos, logo and decorative artwork. A replacement is shared wherever
  that image appears. Clear the replacement to restore the original.

Image fields include a preview and crop controls. Choose a file, drag the preview
to position it, and use Zoom and Frame to crop. Save to apply the crop. You can
also crop an already uploaded image without uploading it again. Cropping saves
a new PNG and keeps the previous stored file. Reset crop saves the full selected
image instead. PNG, JPG, WebP and GIF can be cropped (animated images become a
single frame); SVG artwork can be replaced but cannot be cropped. The website's
existing containers and responsive layout keep their dimensions.
Use Homepage photo in Site settings for the main hero, Rooms for each room's
photo, and Activities for each activity's photo. Site images controls their
bundled fallback images. Admin changes update the live Django site immediately;
the standalone frontend preview still requires a fresh export.

Owner-provided content is recorded in migration 0003: three rooms (up to 11 guests), eight activities, included breakfast/yoga/community/bikes, optional paid dinner, and the supplied Google Maps location link. Policies stay visibly marked as drafts until reviewed and approved in Site settings. Shared Drive assets have not been downloaded because the supplied folder requires sign-in. Upload the confirmed homepage image and brand artwork in Site settings once available.

Uploaded files are served locally during development. Production hosting must serve `/media/` from persistent storage and `/static/` from the collected static files.

## Deploy the live site on Railway

The Dockerfile runs Django with Gunicorn, collects CSS/images for WhiteNoise,
and applies database migrations at startup. Deploy this repository's root;
remove any Railway build/start override that runs Vite or `npm run preview`.

1. Add a **PostgreSQL** service and a **Storage Bucket** to your Railway project.
2. In the website service's Variables, set:

   | Variable | Value |
   | --- | --- |
   | `DJANGO_DEBUG` | `false` |
   | `DJANGO_SECRET_KEY` | A random secret, generated with the command below |
   | `DATABASE_URL` | Reference the Postgres service's `DATABASE_URL` using Railway's variable picker |
   | `AWS_STORAGE_BUCKET_NAME` | Bucket name from the bucket credentials |
   | `AWS_ACCESS_KEY_ID` | Bucket access key |
   | `AWS_SECRET_ACCESS_KEY` | Bucket secret key |
   | `AWS_S3_ENDPOINT_URL` | Bucket HTTPS endpoint |
   | `AWS_S3_REGION_NAME` | Region shown in the bucket credentials (default: `auto`) |
   | `AWS_S3_ADDRESSING_STYLE` | `virtual` (default); use `path` only if the bucket Credentials tab specifies path-style URLs |

   Generate a secret locally: `.venv/bin/python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`.
   Keep credentials in Railway Variables, never in Git or chat.
3. Under the website service's Settings → Networking, generate a public domain.
   Railway's `RAILWAY_PUBLIC_DOMAIN` is allowed automatically. For a custom domain,
   add `DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com` and
   `DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com`.
4. Push these changes and deploy. Logs should show successful migrations and
   Gunicorn listening on Railway's port.
5. In Railway's SSH shell for the running website service, run
   `python manage.py createsuperuser`, then sign in at `https://YOUR-DOMAIN/admin/`.
6. Upload a photo in Site settings or Rooms. Check the homepage, Villa,
   Activities, admin styles and photo. Redeploy and confirm the uploaded photo
   and edited text still appear. This checks persistence in both services.

Postgres stores content and photo filenames; the bucket stores the actual files.
Private bucket photos load through signed URLs generated when Django renders a
page. Existing bundled photos stay in the app's collected static assets.
The initial migrations seed starter content, but they do **not** transfer later
edits from your local SQLite database or existing local uploads. Re-enter those
through admin, or export/import them separately before switching to production.
Configure database backups in Railway and keep separate backups of uploaded photos.

## Standalone frontend preview

```bash
.venv/bin/python scripts/export_frontend.py
npm run dev
```

The Vite version is an exported snapshot, not the live admin-backed site. After an admin edit, rerun the export to update this preview. For a built preview:

```bash
.venv/bin/python scripts/export_frontend.py
npm run build
npm run preview
```

Both versions include the core styles directly in the page. The npm dev/build scripts automatically sync stylesheet changes. Optional Google Maps content loads after the visitor enables it; the footer preference control can disable it again. No analytics or advertising scripts are included.
