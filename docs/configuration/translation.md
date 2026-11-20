# Using Transifex to translate your plugin

Transifex support is optional. Install it with:

```bash
pip install 'qgis-plugin-ci[transifex]'
```

This also installs PyQt, which provides `pylupdate5`, used to extract the strings to translate.
If needed, set its path with `pylupdate5_path` in the configuration.

```yaml
jobs:
  include:
    - stage: push-translation
      if: branch = main
      script: qgis-plugin-ci push-translation ${TX_TOKEN}

    - stage: deploy
      if: tag IS present
      script:
        - >
          qgis-plugin-ci release ${CI_COMMIT_TAG}
          --transifex-token ${TX_TOKEN}
          --github-token ${GH_TOKEN}
          --osgeo-username ${OSGEO_USERNAME}
          --osgeo-password ${OSGEO_PASSWORD}
```
