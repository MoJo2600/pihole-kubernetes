# Changelog

## [2.29.0](https://github.com/MoJo2600/pihole-kubernetes/compare/pihole-2.28.0...pihole-2.29.0) (2025-03-07)


### Features

* allow for env map values ([#339](https://github.com/MoJo2600/pihole-kubernetes/issues/339)) ([f6fcb06](https://github.com/MoJo2600/pihole-kubernetes/commit/f6fcb06d4c5d3a5fd41e08d8dbcc7e3fbba68a85))
* bump pihole version to 2025.03.0 ([#352](https://github.com/MoJo2600/pihole-kubernetes/issues/352)) ([83dd678](https://github.com/MoJo2600/pihole-kubernetes/commit/83dd67801fe07f872a12301a96f087b8e9d0f2f1))

## [2.28.0](https://github.com/MoJo2600/pihole-kubernetes/compare/pihole-2.27.0...pihole-2.28.0) (2025-03-02)


### Features

* add custom deployment annotation option ([#332](https://github.com/MoJo2600/pihole-kubernetes/issues/332)) ([bc8f720](https://github.com/MoJo2600/pihole-kubernetes/commit/bc8f720a9343e8b61fea68b67a2aa4f9ca56c0f4))
* allow to override the command of the cloudflared container. ([#331](https://github.com/MoJo2600/pihole-kubernetes/issues/331)) ([02cff49](https://github.com/MoJo2600/pihole-kubernetes/commit/02cff4992313488524f0883946bb6e425be8be77))
* PiHole v6 Support ([#343](https://github.com/MoJo2600/pihole-kubernetes/issues/343)) ([8112b80](https://github.com/MoJo2600/pihole-kubernetes/commit/8112b800b98eb6ff23aa19d074b56acd72e1066b))
* support doh readiness and podmonitor ([#335](https://github.com/MoJo2600/pihole-kubernetes/issues/335)) ([2c5aaf5](https://github.com/MoJo2600/pihole-kubernetes/commit/2c5aaf592b10d69ce674e87833edb82ad4954110))

## [2.27.0](https://github.com/MoJo2600/pihole-kubernetes/compare/pihole-2.26.2...pihole-2.27.0) (2024-11-28)


### Features

* add command option to set up readiness probe. ([#323](https://github.com/MoJo2600/pihole-kubernetes/issues/323)) ([f5c6ad3](https://github.com/MoJo2600/pihole-kubernetes/commit/f5c6ad3661a2a87e5014aff6c617ea0367177b24))
* add the label app.kubernetes.io/name to deployment and services ([#321](https://github.com/MoJo2600/pihole-kubernetes/issues/321)) ([61ab00d](https://github.com/MoJo2600/pihole-kubernetes/commit/61ab00d1f7fe0cfabfc426bf484cec46fff6ed11))
* configurable pathType for the ingress resource ([#317](https://github.com/MoJo2600/pihole-kubernetes/issues/317)) ([d3c09bc](https://github.com/MoJo2600/pihole-kubernetes/commit/d3c09bc0a6addc487ceda44b516e0714c06c1875))

## [2.26.2](https://github.com/MoJo2600/pihole-kubernetes/compare/pihole-2.26.1...pihole-2.26.2) (2024-10-27)


### Bug Fixes

* wrong customSettings.otherSettings exmaple in values.yaml ([#319](https://github.com/MoJo2600/pihole-kubernetes/issues/319)) ([67a0e3f](https://github.com/MoJo2600/pihole-kubernetes/commit/67a0e3fce49f9899bd92f1fad3ed96ae1148b78e)), closes [#318](https://github.com/MoJo2600/pihole-kubernetes/issues/318)

## [2.26.1](https://github.com/MoJo2600/pihole-kubernetes/compare/pihole-2.26.0...pihole-2.26.1) (2024-07-26)


### Bug Fixes

* Update Notes.txt ([#309](https://github.com/MoJo2600/pihole-kubernetes/issues/309)) ([0c98981](https://github.com/MoJo2600/pihole-kubernetes/commit/0c9898127323effa124aef86f492c3935d8bc017)), closes [#307](https://github.com/MoJo2600/pihole-kubernetes/issues/307)

## [2.26.0](https://github.com/MoJo2600/pihole-kubernetes/compare/pihole-2.25.0...pihole-2.26.0) (2024-07-18)


### Features

* bump pihole version to 2024.07.0 ([#306](https://github.com/MoJo2600/pihole-kubernetes/issues/306)) ([a119d89](https://github.com/MoJo2600/pihole-kubernetes/commit/a119d893c9d193b38875f6b7841855f68716ca32))

## [2.25.0](https://github.com/MoJo2600/pihole-kubernetes/compare/pihole-2.24.0...pihole-2.25.0) (2024-06-27)


### Features

* bump pihole version to 2024.06.0 ([#303](https://github.com/MoJo2600/pihole-kubernetes/issues/303)) ([7f96afc](https://github.com/MoJo2600/pihole-kubernetes/commit/7f96afce866cd2dadfbb7d717ad05b87e23538a4))

## [2.24.0](https://github.com/MoJo2600/pihole-kubernetes/compare/pihole-2.23.0...pihole-2.24.0) (2024-05-14)


### Features

* bump pihole version to 2024.05.0 ([#298](https://github.com/MoJo2600/pihole-kubernetes/issues/298)) ([2b9fada](https://github.com/MoJo2600/pihole-kubernetes/commit/2b9fada9ea76857e9641935a7637a317451751cd))

## [2.23.0](https://github.com/MoJo2600/pihole-kubernetes/compare/pihole-2.22.0...pihole-2.23.0) (2024-04-04)


### Features

* Add optional annotations to the password secret ([#287](https://github.com/MoJo2600/pihole-kubernetes/issues/287)) ([b71d543](https://github.com/MoJo2600/pihole-kubernetes/commit/b71d54321e4c78f2640e0bbd979f3ebe840b2660))
* bump pihole version to 2024.03.2 Bump program version [Workflow Run]: https://github.com/MoJo2600/pihole-kubernetes/actions/runs/8555143588 ([#294](https://github.com/MoJo2600/pihole-kubernetes/issues/294)) ([6e9bd88](https://github.com/MoJo2600/pihole-kubernetes/commit/6e9bd882a0df505468bcdee2a3a476e2fb39058d))


### Bug Fixes

* invalid web service manifest generation ([#288](https://github.com/MoJo2600/pihole-kubernetes/issues/288)) ([b1019dc](https://github.com/MoJo2600/pihole-kubernetes/commit/b1019dcdd2b3f42ba05dbca8b687ee2627d92411))
* Update Chart.yaml ([#291](https://github.com/MoJo2600/pihole-kubernetes/issues/291)) ([f10c1fc](https://github.com/MoJo2600/pihole-kubernetes/commit/f10c1fca167346de4fbd6681cfebd08cae7c13df))

## [2.22.0](https://github.com/MoJo2600/pihole-kubernetes/compare/pihole-v2.28.0...pihole-2.22.0) (2024-02-16)


### Features

* add support for service extraLabels ([#266](https://github.com/MoJo2600/pihole-kubernetes/issues/266)) ([4a09a58](https://github.com/MoJo2600/pihole-kubernetes/commit/4a09a5839e35d075598343bdf138161cf4ed5da7))
* Bump pihole version to 2024.02.0 ([#283](https://github.com/MoJo2600/pihole-kubernetes/issues/283)) ([f9ec0af](https://github.com/MoJo2600/pihole-kubernetes/commit/f9ec0af000d6e4724010e5c18004896031485450))
* Change to trigger a new Release ([#280](https://github.com/MoJo2600/pihole-kubernetes/issues/280)) ([dea65aa](https://github.com/MoJo2600/pihole-kubernetes/commit/dea65aa7d2e17336c63cb4ee8fdbb5f13eceaab6))

## [2.28.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.15...pihole-2.28.0) (2024-01-22)


### Features

* Bump pihole version to 2024.01.0 ([#69](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/69)) ([4954679](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/49546795430caa09ae7d2739fc2710650e5a753e))
* documentation ([7902fa0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/7902fa03627cf7f1643bb5fcf71fe473d2725058))

## [2.27.15](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.14...pihole-2.27.15) (2024-01-22)


### Bug Fixes

* pipeline ([cd5c934](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/cd5c934099b40921a05e5657b068d735b19aa5a5))
* version ([cfdc6a8](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/cfdc6a8b59c7848520b0a33414d0aecfa6d0e38f))

## [2.27.14](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.13...pihole-2.27.14) (2024-01-22)


### Bug Fixes

* docu ([9d4cf11](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/9d4cf111dabf42ff4e924e77357f24b410702264))
* docu ([2d1c7de](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/2d1c7de714eba1d311db699e2f59f8e20a65814a))

## [2.27.13](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.12...pihole-2.27.13) (2024-01-22)


### Bug Fixes

* docu ([c52c82c](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/c52c82c321b5cef5224d92209f7c5c87c3ac30d0))

## [2.27.12](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.11...pihole-2.27.12) (2024-01-22)


### Bug Fixes

* docu ([26298d4](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/26298d4fa18fe5b4c1b5b6fee0c35768f749ccfd))

## [2.27.11](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.10...pihole-2.27.11) (2024-01-22)


### Bug Fixes

* docu ([ba0e068](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/ba0e0685dfa5aa457b0199faac8640ae6426ed31))

## [2.27.10](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.9...pihole-2.27.10) (2024-01-22)


### Bug Fixes

* docu ([357a35e](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/357a35e7ea3420b13812115680702bc99cc88b7c))
* docu ([7ee22ef](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/7ee22effee65aa243c530bb91cbb79ac96edb28c))

## [2.27.9](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.8...pihole-2.27.9) (2024-01-22)


### Bug Fixes

* documentation ([a667641](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/a6676416755a998cbc92172ae8850bacf7bfcf23))

## [2.27.8](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.7...pihole-2.27.8) (2024-01-22)


### Bug Fixes

* docu ([044794e](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/044794e56d7cb4062f1d448f5b4ab53d1d2bfb97))

## [2.27.7](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.6...pihole-2.27.7) (2024-01-22)


### Bug Fixes

* docu ([5319065](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/53190650a860caba1f4db78ad6bd3bfde814b83c))
* documentation ([28b59be](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/28b59be0b29e564b3f8e3b0d63fc117280ee4959))
* pipeline ([f94cb6a](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/f94cb6a0a1c028627eac6002c227dff51383c655))

## [2.27.6](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.5...pihole-2.27.6) (2024-01-22)


### Bug Fixes

* documentation ([6e73f70](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/6e73f70d1e8ea2cd8d8be222872f53ff2ba39cfa))
* documentation ([5d0e28d](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/5d0e28d8e2e980c5759dda885a96a0036b9a773f))
* documentation ([767adf6](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/767adf6b19d4e888bafd1f1eb3cc302cfa8770de))

## [2.27.5](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.4...pihole-2.27.5) (2024-01-22)


### Bug Fixes

* documentation ([e031bf3](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/e031bf330de12dd6cc40163c7c58337e30d045ca))

## [2.27.4](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.3...pihole-2.27.4) (2024-01-22)


### Bug Fixes

* chart ([eb77bd6](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/eb77bd6e5f0faa548a58d9f4a55b3b08b384370b))
* documentation ([c33a323](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/c33a3239b6eb074194e4161b0c6a416098b5f985))

## [2.27.3](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.2...pihole-2.27.3) (2024-01-19)


### Bug Fixes

* reasdf ([#52](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/52)) ([1614b4f](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/1614b4f01333e7d974a09c7cad99c43e4ab9e013))

## [2.27.2](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.1...pihole-2.27.2) (2024-01-19)


### Bug Fixes

* reasdf ([#50](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/50)) ([a189de9](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/a189de95b50683313ae71bb02709e1af0ff49c10))

## [2.27.1](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.27.0...pihole-2.27.1) (2024-01-19)


### Bug Fixes

* release worthy ([#48](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/48)) ([89f2b67](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/89f2b679ae4628069d3237ff4bf60c80841f4506))

## [2.27.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.26.0...pihole-2.27.0) (2024-01-19)


### Features

* new value ([#46](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/46)) ([9f350de](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/9f350de18ca5dafbcd71ed6c295970ab5bbf4024))

## [2.26.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.25.5...pihole-2.26.0) (2024-01-18)


### Features

* nonsemantic release ([#44](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/44)) ([0949c23](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/0949c2378c9002c31ed64ffad2d85ffbb35e9240))
* semantic pr title check ([#43](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/43)) ([0bb7787](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/0bb7787ce6bcf7ff8000e9fcf462dfde6d978a69))


### Bug Fixes

* add prepare ([fc3d3ed](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/fc3d3edadb99c10e9372f74ad00a4669ee631704))
* another fix ([fd147a9](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/fd147a9304755dc06f5bde2e300dfe995e3b76bb))

## [2.25.5](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.25.4...pihole-2.25.5) (2024-01-18)


### Bug Fixes

* user facing change ([c0b8572](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/c0b85721d31d7ea7ad4fd952944bec6b8179aa52))

## [2.25.4](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.25.3...pihole-2.25.4) (2024-01-18)


### Bug Fixes

* changes were made ([126f99a](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/126f99a012c8acaacd83943b2c59273959ab6e44))
* split release-please steps ([e6c299c](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/e6c299c39b3b3faa04373268067e9c63fe6f4769))
* split release-please steps 3 ([68061ef](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/68061ef7f00fe5b8d736e1d67fe7cddff17fbd88))
* update readme ([1e1da72](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/1e1da7287b47094082077e4a4e070c47b72b97cc))

## [2.25.3](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.25.2...pihole-2.25.3) (2024-01-17)


### Bug Fixes

* documentation add ([216d9a0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/216d9a0b09ca20338728c29c4137b61d938c4e27))

## [2.25.2](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.25.1...pihole-2.25.2) (2024-01-17)


### Bug Fixes

* docu ([19775ae](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/19775ae1c56767a52423b29560cccc76e5210f59))
* dudeldidum ([#37](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/37)) ([771b66b](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/771b66b58234e351383e5c9ba6ff2319a3bc8e41))
* extra-files ([7fd4659](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/7fd465958db3c217d728bfe04fe3a728e90af2b1))
* more stuff ([21b6f50](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/21b6f500f3416bbbcdd887257faed98d6270e6b8))
* version string ([37b0726](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/37b0726952ee3368394857ceba72b354b1da53c9))

## [2.25.1](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.25.0...pihole-2.25.1) (2024-01-17)


### Bug Fixes

* update workflow ([b34a376](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/b34a3763d1e729180ed6e12c62d8b35e6257a9a6))

## [2.25.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.24.1...pihole-2.25.0) (2024-01-17)


### Features

* add workflow ([2e6b419](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/2e6b419d7feae0e44c7f3c4d3c6d8dd9c5cb1aba))


### Bug Fixes

* deplyoment ([51c4de2](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/51c4de263207464fa4530108a96b78d39fb88554))
* docu ([cebbe86](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/cebbe860ae67da8ecfa3dcfcd6f2523cddc959c8))
* docu ([315ba58](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/315ba587f16942c30d57c4bbbe2f326985a25433))
* docu ([#31](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/31)) ([e922ee7](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/e922ee73eb88b5e30e8e33b2fc92f4ac9bb45743))
* documentation ([1e11b06](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/1e11b064a1a03245fbbfc38e9c5eeffdfeed1555))
* documentation ([f4eb84d](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/f4eb84da543272b7945a1b8d196a6487c38a0a8f))
* documentation ([780df0d](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/780df0d9d5c1dbb455c17a08837fda6dafc42af7))
* documentation ([#32](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/32)) ([28c05e1](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/28c05e194f4dc63619ac9aba7a7bf6177c25d843))
* foo ([2d48537](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/2d485377272cbcff78f50eb3076df9510a8fea9b))

## [2.24.1](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.24.0...pihole-2.24.1) (2023-10-26)


### Bug Fixes

* test ([368b29d](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/368b29d72b7eb40058a6723cb12a118ae80a335f))

## [2.24.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-v2.23.2...pihole-2.24.0) (2023-10-26)


### Features

* chart change ([b97b4f1](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/b97b4f17c689a8e7a782820366501eb3f3d47822))
* chart change ([#27](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/27)) ([79caa0a](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/79caa0a2b868d92b5181071b67e268d81e460ce2))
* chart change more docu ([ee97a50](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/ee97a50bb986e12acac90c0f6ae23d1ee3bd8f11))
* more documentation ([14b6386](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/14b6386825725053455bbb1bbec4b47b95bb7a0a))
* more documentation ([ab229d7](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/ab229d7c6fb8654a1d13bcfacf79b33dfc8e1233))
* release-please ([c084b92](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/c084b92fd3cca0f45a43be384c4394d8ee066cec))


### Bug Fixes

* more documentation ([ab229d7](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/ab229d7c6fb8654a1d13bcfacf79b33dfc8e1233))
* more documentation ([061aab8](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/061aab85983c6e3adc853e68b3e96277c39659a5))
* release ([6dd7615](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/6dd7615e603bba728ce1edcffac8361ddb18ddf4))

## [2.23.1](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.23.0...pihole-2.23.1) (2023-05-17)


### Bug Fixes

* release ([6dd7615](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/6dd7615e603bba728ce1edcffac8361ddb18ddf4))

## [2.23.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.22.0...pihole-2.23.0) (2023-05-17)


### Features

* chart change ([b97b4f1](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/b97b4f17c689a8e7a782820366501eb3f3d47822))

## [2.22.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.21.0...pihole-2.22.0) (2023-05-17)


### Features

* chart change more docu ([ee97a50](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/ee97a50bb986e12acac90c0f6ae23d1ee3bd8f11))

## [2.21.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.20.0...pihole-2.21.0) (2023-05-17)


### Features

* more documentation ([14b6386](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/14b6386825725053455bbb1bbec4b47b95bb7a0a))

## [2.20.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-v2.19.0...pihole-2.20.0) (2023-05-17)


### Features

* more documentation ([ab229d7](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/ab229d7c6fb8654a1d13bcfacf79b33dfc8e1233))


### Bug Fixes

* more documentation ([ab229d7](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/ab229d7c6fb8654a1d13bcfacf79b33dfc8e1233))
* more documentation ([061aab8](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/061aab85983c6e3adc853e68b3e96277c39659a5))

## [2.19.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-v2.18.0...pihole-v2.19.0) (2023-05-04)


### Features

* release-please ([c084b92](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/c084b92fd3cca0f45a43be384c4394d8ee066cec))

## [2.18.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-v2.17.0...pihole-v2.18.0) (2023-05-02)


### Features

* more docu3 ([#8](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/8)) ([a8ac693](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/a8ac69371a794779bbbfc832509e5edd2d5d3708))
* more docu4 ([#10](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/10)) ([e371a33](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/e371a3307d72209203cfd3912874483d1982a9d6))
* more documentation ([#5](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/5)) ([90d4703](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/90d4703f40349fcfc0464d2e1631254ffac8f077))
* new build pipeline ([c3a7d71](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/c3a7d714b332ee4de7e41947b78b35eb77cd1bbf))
* release please test ([#6](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/6)) ([886eac4](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/886eac4d8af189606ce6c8c42470a3cd8cf7b3aa))
* release please test asdf ([#12](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/12)) ([005679e](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/005679ec9debc74ae590f0897420024b50e8d8c0))

## [2.17.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-2.16.0...pihole-v2.17.0) (2023-05-02)


### Features

* release please test asdf ([#12](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/12)) ([005679e](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/005679ec9debc74ae590f0897420024b50e8d8c0))

## [2.16.0](https://github.com/MoJo2600/pihole-kubernetes-githubactions/compare/pihole-v2.15.0...pihole-v2.16.0) (2023-04-28)


### Features

* more docu3 ([#8](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/8)) ([a8ac693](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/a8ac69371a794779bbbfc832509e5edd2d5d3708))
* more docu4 ([#10](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/10)) ([e371a33](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/e371a3307d72209203cfd3912874483d1982a9d6))
* more documentation ([#5](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/5)) ([90d4703](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/90d4703f40349fcfc0464d2e1631254ffac8f077))
* new build pipeline ([c3a7d71](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/c3a7d714b332ee4de7e41947b78b35eb77cd1bbf))
* release please test ([#6](https://github.com/MoJo2600/pihole-kubernetes-githubactions/issues/6)) ([886eac4](https://github.com/MoJo2600/pihole-kubernetes-githubactions/commit/886eac4d8af189606ce6c8c42470a3cd8cf7b3aa))
