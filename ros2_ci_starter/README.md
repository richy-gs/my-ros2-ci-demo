# ros2_ci_starter

A minimal ROS 2 workspace wired up with the same GitHub Actions pipeline
pattern used in most robotics labs and companies: **lint → build → test →
publish artifacts**, gated on every pull request.

Use this as a template. Push it to a new GitHub repo, watch the pipeline run,
then start breaking and fixing things — that's the fastest way to actually
learn CI/CD.

## Why this exists

In a robotics job, "CI/CD" almost never means deploying to a real robot on
every commit (that's dangerous). It usually means:

1. **CI (Continuous Integration)** — every push/PR automatically:
   - lints the code (style, copyright headers, static analysis)
   - builds the workspace with `colcon`
   - runs unit + integration tests with `colcon test`
   - reports results back on the PR, blocking merge if anything fails
2. **CD (Continuous Delivery/Deployment)** — once code lands on `main`:
   - a Docker image or Debian package is built and versioned
   - it's pushed to a registry (GHCR, ECR, a company artifactory)
   - a human (or a fleet-management tool) decides when to roll it out to
     hardware — actual "deploy to the robot" is usually a separate, manual
     or staged step, not automatic

This repo implements step 1 fully, and step 2 as an optional extension
(see "Going further" below).

## Repo layout

```
ros2_ci_starter/
├── .github/workflows/
│   ├── ci.yml            # build + colcon test, matrix over ROS distros
│   └── lint.yml          # ament linters (flake8, pep257, copyright, xmllint)
├── .pre-commit-config.yaml  # same checks, run locally before you even push
├── .gitignore
└── src/
    └── demo_pkg/          # a tiny real ROS 2 package (ament_python)
        ├── package.xml
        ├── setup.py / setup.cfg
        ├── demo_pkg/talker.py     # a publisher node
        ├── launch/demo_launch.py
        └── test/                 # pytest + ament lint tests
```

`demo_pkg` is deliberately trivial (one publisher node) — the point of this
repo is the pipeline around it, not the robotics logic. Swap in your own
packages once you understand the flow.

## 1. Turn this into your own GitHub repo

```bash
cd ros2_ci_starter
git init
git add .
git commit -m "Initial commit: ROS 2 workspace with CI"
gh repo create my-ros2-ci-demo --public --source=. --push
# no gh CLI? create an empty repo on github.com, then:
# git remote add origin git@github.com:<you>/<repo>.git
# git branch -M main
# git push -u origin main
```

Open the **Actions** tab on GitHub — you should see `CI` and `Lint` running
automatically, because the workflows trigger on `push` and `pull_request`.

## 2. Make CI actually gate your merges

This is the part most tutorials skip, and it's the part that matters most in
a real team:

1. GitHub repo → **Settings → Branches → Add branch protection rule**
2. Branch name pattern: `main`
3. Enable **Require a pull request before merging**
4. Enable **Require status checks to pass before merging**, then select the
   `build-and-test` and `ament_*` jobs once they've run at least once
5. (Optional but standard in most labs) **Require branches to be up to date
   before merging**

Now nobody — including you — can push straight to `main`, and a red CI run
physically blocks a merge. That's the core discipline CI/CD is teaching you.

## 3. The actual dev loop

```bash
git checkout -b feature/add-listener-node
# edit code in src/demo_pkg/...
colcon build --symlink-install     # build locally (needs ROS 2 installed)
colcon test && colcon test-result --verbose
git push -u origin feature/add-listener-node
gh pr create --fill
```

Open the PR on GitHub — CI runs automatically, checks appear inline, and you
can't merge until they're green (because of the branch protection rule above).

## How the workflows work

**`ci.yml`** uses two actions maintained by the ROS Tooling Working Group,
which is what almost every real ROS 2 project uses instead of hand-rolling
`apt install` + `rosdep` + `colcon` steps:

- [`ros-tooling/setup-ros`](https://github.com/ros-tooling/setup-ros) —
  installs ROS 2 (or spins up the right Docker image) on the runner
- [`ros-tooling/action-ros-ci`](https://github.com/ros-tooling/action-ros-ci) —
  assembles a workspace, resolves dependencies with `rosdep`, then runs
  `colcon build` and `colcon test` for the package you name

It runs on a matrix (`ros_distro: [jazzy]`) — add `humble` or `kilted` to
that list if you need to support more than one distro, the same way a real
project supports multiple Ubuntu/ROS versions at once.

**`lint.yml`** runs the same `ament_*` linters that `colcon test` runs
locally (flake8, pep257, copyright headers, XML validity) as separate,
faster jobs — so style problems fail fast without waiting for a full build.

**`.pre-commit-config.yaml`** lets you catch the same issues *before* you
even push, with `pip install pre-commit && pre-commit install`. Most labs
require this in their CONTRIBUTING.md so CI failures are rare rather than
routine.

## Going further (what a real robotics team adds next)

Roughly in the order teams usually add them:

- **Code coverage** — `colcon test` + `lcov`/`gcovr`, upload to Codecov
- **Docker image build** — build a runtime image on merge to `main`, push to
  GitHub Container Registry (`ghcr.io`), tag with the git SHA
- **Multi-distro / multi-arch matrix** — add `arm64` (Jetson boards) via
  QEMU or self-hosted ARM runners
- **Hardware-in-the-loop or simulation tests** — spin up Gazebo/Ignition in
  CI, or run a nightly job on a self-hosted runner attached to real hardware
- **Nightly/rolling builds** — a scheduled workflow (`on: schedule`) against
  ROS 2 `rolling`, to catch upstream breakage early
- **Semantic versioning + changelog** — tools like `release-please` to cut
  versioned releases automatically from conventional commits
- **Staged deployment** — a separate, manually-triggered workflow
  (`workflow_dispatch`) that pushes a new image to a fleet-management system,
  never automatic on every merge

You don't need any of that to learn the core loop — get the basic
lint/build/test pipeline green and merge-gated first, then add one of these
at a time.

## Requirements to build locally

- Ubuntu 24.04 + ROS 2 Jazzy (or use the `osrf/ros:jazzy-desktop` Docker
  image) — matches what `ci.yml` runs in CI
- `colcon` (`sudo apt install python3-colcon-common-extensions`)
