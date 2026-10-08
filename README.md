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

- **Site settings:** homepage title, description and photo; brand illustration; booking link; business and contact details; editable policies and owner approval status.
- **Rooms:** names, descriptions, photos and ordering. All rooms appear on the site.
- **Activities:** names, descriptions, photos, symbols and ordering. All activities appear on the site.
- **Blog posts:** archive stories, categories, publication status and ordering.

Owner-provided content is recorded in migration 0003: three rooms (up to 11 guests), eight activities, included breakfast/yoga/community/bikes, optional paid dinner, and the supplied Google Maps location link. Policies stay visibly marked as drafts until reviewed and approved in Site settings. Shared Drive assets have not been downloaded because the supplied folder requires sign-in. Upload the confirmed homepage image and brand artwork in Site settings once available.

Uploaded files are served locally during development. Production hosting must serve `/media/` from persistent storage and `/static/` from the collected static files.

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
