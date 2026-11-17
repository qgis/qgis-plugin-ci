# Using Transifex to translate your plugin

## Configuration

```toml
translation_languages = [
    "my_MM",
    "zh",
]
```

## Local TS files



## Transifex

Transifex support is optional. Install it with:

```bash
pip install 'qgis-plugin-ci[transifex]'
```

This also installs PyQt, which provides `pylupdate`, used to extract the strings to translate.
If needed, set its path with `pylupdate_path` in the configuration.

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
          qgis-plugin-ci release ${TRAVIS_TAG}
          --transifex-token ${TX_TOKEN}
          --github-token ${GH_TOKEN}
          --osgeo-username ${OSGEO_USERNAME}
          --osgeo-password ${OSGEO_PASSWORD}
```
