# GitHub Pages build

A push to `main`, or a manual run of the **Build and deploy playable chapter** workflow from `main`, imports and tests the project, exports the single-threaded Godot Web build, and publishes the build through GitHub Pages. The `development` branch is for ongoing work; changes appear on Pages after they are merged into `main`.

The repository's Pages publishing source must be set to **GitHub Actions**. The workflow uses the official Godot 4.6.3 release, verifies the editor and the selected Web template against recorded SHA-256 values, and caches the template. The first run downloads the full official export-template archive before extracting the one required file; later runs reuse the cache. Test failures stop deployment.

The workflow deployment URL and run result are the source of truth for whether a build is live. Browser saves belong to the site's origin and browser profile, and differ from saves made on localhost.
