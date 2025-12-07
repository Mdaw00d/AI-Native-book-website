# Implementation Plan: Vision-Language-Action (VLA) Integration

**Spec Reference:** `specs/1-vla-integration/spec.md`
**Created:** 2025-12-07
**Architect:** Mdaw00d

## Executive Summary

This plan outlines the implementation approach for creating educational content teaching Vision-Language-Action integration. The content will be delivered as Docusaurus-based documentation with embedded Jupyter notebooks, standalone Python scripts, and a containerized ROS 2 simulation environment. Learners will progress through 10 structured sections culminating in a capstone project where a simulated humanoid robot executes voice commands end-to-end.

## Scope & Dependencies

### In Scope

- 10 educational content sections (Markdown documentation)
- Interactive Jupyter notebooks for component tutorials
- Standalone Python scripts for capstone project
- Docker container with ROS 2 Humble + Gazebo + pre-configured robot
- Code examples covering speech recognition, LLM planning, computer vision, navigation, manipulation
- Diagrams, videos, and interactive demonstrations
- Automated testing and validation pipeline
- Accessibility compliance (WCAG 2.1 AA)

### Out of Scope

- Physical robot hardware integration
- Custom model training (speech, vision, or LLM)
- Real-time performance optimization beyond educational demonstration
- Cloud-based simulation infrastructure
- Multi-language localization (English only initially)

### External Dependencies

| Dependency | Version | Owner | Status |
|------------|---------|-------|--------|
| Docusaurus | 3.9.2 | Meta OSS | Active |
| ROS 2 Humble | LTS | Open Robotics | Active (LTS until 2027) |
| Gazebo Garden | Latest | Open Robotics | Active |
| OpenAI API | GPT-4 | OpenAI | Active |
| Whisper | Latest | OpenAI | Active (open source) |
| YOLOv8 | Latest | Ultralytics | Active |
| Nav2 | Humble | Nav2 Team | Active |
| MoveIt 2 | Humble | PickNik Robotics | Active |
| Docker | Latest | Docker Inc. | Active |

## Key Architectural Decisions

### Decision 1: LLM Provider for Cognitive Planning

**Context:**
The VLA module requires an LLM to convert natural language commands into structured ROS 2 action sequences. The choice affects learner experience, setup complexity, and cost.

**Options Considered:**

1. **OpenAI GPT-4 (API-based)**
   - Pros: Excellent structured output support (JSON mode), strong reasoning, widely used in industry, simple API integration
   - Cons: Requires API key and billing, internet dependency, potential rate limits

2. **Local LLMs (Llama 3.1, Mistral via Ollama)**
   - Pros: No API costs, offline capability, privacy, full control
   - Cons: Requires 16GB+ RAM, slower inference on CPU, inconsistent structured output quality

3. **Rule-based command parser**
   - Pros: Deterministic, no external dependencies
   - Cons: Limited flexibility, misses educational value of LLM integration, brittle

**Decision:** OpenAI GPT-4 as primary, with Ollama + Llama 3.1 as documented alternative

**Rationale:**
- **Educational Priority**: Learning LLM integration is a core objective; rule-based parsing defeats the purpose
- **Accessibility**: GPT-4 API is easier for beginners than local LLM setup
- **Structured Output**: GPT-4's JSON mode ensures reliable machine-readable task plans
- **Fallback Option**: Documenting Ollama path provides offline alternative for advanced learners

**Reversibility:** Easy - LLM interface abstracted behind Python class, swappable implementation

---

### Decision 2: Simulation Environment Delivery

**Context:**
ROS 2 + Gazebo setup is complex (20+ packages, specific versions, OS dependencies). This is the highest risk for learner drop-off.

**Options Considered:**

1. **Docker Container (multi-stage with ROS 2 Humble + Gazebo)**
   - Pros: Cross-platform, reproducible, fast setup (~10 min), version-locked dependencies
   - Cons: Requires Docker knowledge, X11 forwarding complexity on macOS/Windows

2. **Manual Installation Instructions**
   - Pros: Learners understand each component, no containerization overhead
   - Cons: High failure rate (est. 20-30%), platform-specific issues, time-consuming (1-2 hours)

3. **Virtual Machine Image**
   - Pros: Complete pre-configured environment
   - Cons: Large download (8-12GB), slow startup, high resource requirements (16GB+ RAM)

4. **Cloud-based Simulation (Gazebo Web)**
   - Pros: Zero local setup, instant access
   - Cons: Internet requirement, limited customization, ongoing hosting costs

**Decision:** Docker container as primary method, with manual installation as "deep dive" optional path

**Rationale:**
- **Risk Mitigation**: Addresses #1 identified risk (simulation complexity)
- **Success Metric**: Enables <10 min setup supporting "<10% setup failure rate" goal
- **Cross-Platform**: Works on Linux, macOS (Docker Desktop), Windows (WSL2)
- **Reversibility**: Learners can inspect Dockerfile and manually install if desired

**Container Architecture:**
```
ros:humble-desktop-full (base)
  → + Gazebo Garden + Nav2 + MoveIt 2 (simulation layer)
  → + Python deps (whisper, openai, ultralytics) (VLA layer)
  → + Robot URDF + demo worlds + code samples (example layer)
```

**Reversibility:** Easy - Dockerfile is transparent, learners can choose manual path

---

### Decision 3: Code Example Format

**Context:**
Need to balance interactive learning (tutorial phase) with production patterns (capstone phase).

**Options Considered:**

1. **Jupyter Notebooks only**
   - Pros: Interactive, inline outputs, great for tutorials
   - Cons: Not representative of production ROS code

2. **Python scripts only**
   - Pros: Production-like, simpler tooling
   - Cons: Less interactive, harder for beginners to debug

3. **Hybrid: Notebooks for tutorials + Scripts for capstone**
   - Pros: Progressive complexity, interactive learning → production transition
   - Cons: More files to maintain, learners must understand both formats

**Decision:** Hybrid approach - Jupyter notebooks for Sections 2-8, standalone Python scripts for Section 9 (capstone)

**Rationale:**
- **Pedagogical Progression**: Notebooks support step-by-step learning; scripts demonstrate integration
- **Learning Objective Alignment**: "Debug and validate multi-modal systems" requires understanding both contexts
- **Industry Practice**: Prototyping in notebooks, production in scripts mirrors real workflows

**File Structure:**
```
code-examples/
├── notebooks/        # Sections 2-8 tutorials
├── scripts/          # Section 9 capstone + reusable modules
├── tests/            # Automated validation
└── requirements.txt  # Unified dependencies
```

**Reversibility:** Easy - notebooks can be converted to scripts (nbconvert), scripts can be imported into notebooks

---

### Decision 4: Object Detection Model

**Context:**
Need real-time object detection that runs on CPU for accessibility and integrates with ROS 2/Gazebo.

**Options Considered:**

1. **YOLOv8n (Ultralytics)**
   - Pros: Real-time on CPU, high accuracy (mAP 37.3), simple API, active development
   - Cons: Larger model size than MobileNet

2. **MobileNet SSD**
   - Pros: Very lightweight, fast inference
   - Cons: Lower accuracy (mAP ~22), older architecture, less educational value

3. **Faster R-CNN**
   - Pros: Highest accuracy
   - Cons: Too slow for real-time demos, GPU requirement

**Decision:** YOLOv8n (nano variant)

**Rationale:**
- **Performance**: Runs real-time on CPU (critical for no-GPU requirement NFR-4)
- **Accuracy**: COCO-pretrained weights cover common manipulation objects
- **Educational Value**: Current industry standard, strong documentation
- **Integration**: Simple Python API works seamlessly with ROS 2 image messages

**3D Pose Estimation Approach:**
- RGB-D camera in Gazebo provides depth
- Bounding box center + depth → 3D position
- PCA on point cloud → orientation (educational simplification)

**Reversibility:** Moderate - detector interface can be swapped, but 3D estimation logic may need adjustment

---

### Decision 5: Content Validation Pipeline

**Context:**
Must ensure all code examples work, links aren't broken, accessibility standards met, before publishing.

**Options Considered:**

1. **Manual Testing Only**
   - Pros: Human judgment, flexible
   - Cons: Time-consuming, error-prone, not scalable

2. **Automated CI Pipeline (GitHub Actions)**
   - Pros: Fast feedback, consistent, blocks bad merges
   - Cons: Setup overhead, requires test writing discipline

3. **Hybrid: Automated gates + manual review**
   - Pros: Catches technical issues automatically, human validates pedagogy
   - Cons: More process overhead

**Decision:** Automated CI pipeline with mandatory gates + optional manual review

**Quality Gates (all must pass before merge):**
1. Markdown linting (markdownlint)
2. Code execution tests (pytest in Docker container)
3. Accessibility scan (axe-core, pa11y-ci)
4. Link validation (markdown-link-check)
5. Build success (Docusaurus build)
6. Performance check (Lighthouse CI, score > 90)

**Manual Review (recommended but not blocking):**
- Pedagogical flow review
- Technical accuracy verification by SME

**Rationale:**
- **Constitution Alignment**: Technical Accuracy principle requires validation
- **Success Metric**: "Code examples tested successfully" requires automated verification
- **Efficiency**: Automation catches regressions faster than manual testing

**Reversibility:** Easy - CI can be disabled, gates can be made advisory vs. blocking

---

## Implementation Phases

### Phase 1: Infrastructure Setup

**Goal:** Establish Docker environment, project structure, and CI pipeline

**Deliverables:**
- [ ] Multi-stage Dockerfile for ROS 2 + Gazebo + VLA dependencies
- [ ] Docker Compose configuration for easy startup
- [ ] Pre-configured robot URDF (humanoid model)
- [ ] Demo Gazebo world (room with objects, obstacles)
- [ ] GitHub Actions CI workflow (lint, test, build, accessibility)
- [ ] Project structure for code examples and docs

**Dependencies:** None (initial phase)

**Risks:**
- **Risk**: Docker image too large (>5GB compressed)
  - **Mitigation**: Multi-stage build, minimal base image, layer optimization
- **Risk**: X11 forwarding issues on macOS/Windows
  - **Mitigation**: Document VcXsrv (Windows) and XQuartz (macOS) setup, provide troubleshooting guide

**Estimated Effort:** 3-4 days

---

### Phase 2: Core Component Development

**Goal:** Create working code examples for each VLA component

**Deliverables:**
- [ ] `voice_interface.py` - Whisper integration with microphone input
- [ ] `llm_planner.py` - GPT-4 task planning with JSON schema validation
- [ ] `ros2_action_client.py` - Navigation goal execution via Nav2
- [ ] `object_detector.py` - YOLOv8 detection with 3D pose estimation
- [ ] `navigation_client.py` - Path planning and obstacle avoidance
- [ ] `manipulation_primitives.py` - Grasp pose generation and execution
- [ ] Corresponding Jupyter notebooks for Sections 2-8
- [ ] Unit tests for each component

**Dependencies:** Phase 1 complete (Docker environment)

**Risks:**
- **Risk**: LLM output variability breaks task execution
  - **Mitigation**: JSON schema validation, retry logic, fallback examples
- **Risk**: Whisper latency too high for "real-time" perception
  - **Mitigation**: Use Whisper small/base models, document expected latency (~1-2s)

**Estimated Effort:** 10-12 days (2-3 days per component pair)

---

### Phase 3: Capstone Integration

**Goal:** Build end-to-end pipeline demonstrating voice → action

**Deliverables:**
- [ ] `full_pipeline.py` - Integrated VLA system
- [ ] State machine for pipeline execution (voice → parse → plan → execute)
- [ ] Logging and visualization of each stage
- [ ] Error handling and recovery strategies
- [ ] Integration tests for multi-step scenarios
- [ ] Demo video of successful capstone execution

**Dependencies:** Phase 2 complete (all components working)

**Risks:**
- **Risk**: Component integration failures (timing, state management)
  - **Mitigation**: Event-driven architecture, clear state transitions, extensive logging
- **Risk**: End-to-end execution time too long for demos
  - **Mitigation**: Simulation fast-forward option, pre-planned scenarios

**Estimated Effort:** 5-6 days

---

### Phase 4: Documentation and Assets

**Goal:** Create all educational content, diagrams, and videos

**Deliverables:**
- [ ] 10 Markdown documentation files (Sections 1-10)
- [ ] Learning objectives, prerequisites, exercises for each section
- [ ] 4-6 architecture diagrams (SVG format)
- [ ] 3-4 demonstration videos (MP4 with captions)
- [ ] Screenshots of key simulation states
- [ ] Glossary of robotics and AI terms
- [ ] Troubleshooting guide for common issues

**Dependencies:** Phase 3 complete (capstone working for video recording)

**Risks:**
- **Risk**: Video file sizes exceed performance budget
  - **Mitigation**: FFmpeg compression, target <5MB/min, host on CDN
- **Risk**: Diagrams not accessible to screen readers
  - **Mitigation**: SVG with titles, descriptive alt text in Markdown

**Estimated Effort:** 8-10 days

---

### Phase 5: Testing and Validation

**Goal:** Ensure all quality gates pass and content is ready for learners

**Deliverables:**
- [ ] All CI checks passing (lint, tests, accessibility, links, build, performance)
- [ ] Accessibility audit complete (WCAG 2.1 AA)
- [ ] Manual walkthrough of all 10 sections by external reviewer
- [ ] Performance validated (Lighthouse > 90, <3s load)
- [ ] Success metrics baseline established (for tracking learner outcomes)

**Dependencies:** Phase 4 complete (all content created)

**Risks:**
- **Risk**: Accessibility violations discovered late
  - **Mitigation**: Incremental a11y testing during Phase 4, automated scans in CI
- **Risk**: Performance issues on 3G connections
  - **Mitigation**: Image/video optimization, lazy loading, throttled testing

**Estimated Effort:** 3-4 days

---

## Interfaces & API Contracts

### LLM Planning Interface

**Input (Natural Language Command):**
```python
{
  "command": str,           # "Navigate to the kitchen and pick up the red cup"
  "environment_context": {  # Optional contextual information
    "known_objects": List[str],
    "known_locations": List[str]
  }
}
```

**Output (Structured Task Plan):**
```python
{
  "tasks": [
    {
      "task_id": int,
      "task_type": str,  # "navigate" | "detect" | "manipulate" | "inspect"
      "parameters": {
        "target": str,
        "location": Optional[str],
        "constraints": List[str]
      },
      "preconditions": List[int],  # task_ids that must complete first
      "expected_duration": float    # seconds (estimate)
    }
  ],
  "feasibility": {
    "is_feasible": bool,
    "confidence": float,        # 0.0-1.0
    "warnings": List[str]
  }
}
```

**Error Handling:**
| Error Type | Condition | User Impact | Recovery Strategy |
|------------|-----------|-------------|-------------------|
| `InvalidCommand` | Unrecognized command structure | Clear error message | Prompt user to rephrase |
| `InfeasibleTask` | Task violates robot constraints | Plan rejected with explanation | Suggest alternative command |
| `LLMTimeout` | API call exceeds 30s | Temporary failure | Retry with exponential backoff (3 attempts) |
| `InvalidSchema` | LLM output doesn't match schema | Validation error | Retry with schema in prompt, fallback to example |

**Versioning:** JSON schema version embedded in output, backward compatible for 1 year

---

### Object Detection Interface

**Input (Camera Image):**
```python
{
  "rgb_image": np.ndarray,    # (H, W, 3) uint8
  "depth_image": np.ndarray,  # (H, W) float32, meters
  "camera_info": {
    "fx": float,              # focal length x
    "fy": float,              # focal length y
    "cx": float,              # principal point x
    "cy": float               # principal point y
  }
}
```

**Output (Detected Objects):**
```python
{
  "detections": [
    {
      "class_name": str,
      "confidence": float,     # 0.0-1.0
      "bbox_2d": {            # Image coordinates
        "x_min": int,
        "y_min": int,
        "x_max": int,
        "y_max": int
      },
      "pose_3d": {            # Robot frame coordinates
        "position": [float, float, float],  # [x, y, z] meters
        "orientation": [float, float, float, float]  # [x, y, z, w] quaternion
      }
    }
  ],
  "processing_time": float   # seconds
}
```

**Error Handling:**
| Error Type | Condition | User Impact | Recovery Strategy |
|------------|-----------|-------------|-------------------|
| `NoDetections` | No objects found above confidence threshold | Empty detections list | Lower threshold or retry |
| `InvalidImage` | Image shape/type mismatch | Processing error | Validate input dimensions |
| `CameraNotCalibrated` | Missing camera_info | 3D pose unavailable | Fall back to 2D detections only |

---

### ROS 2 Navigation Interface

**Input (Navigation Goal):**
```python
{
  "target_pose": {
    "position": [float, float, float],     # [x, y, z] meters
    "orientation": [float, float, float, float]  # [x, y, z, w] quaternion
  },
  "timeout": float,         # seconds
  "tolerance": {
    "position": float,      # meters
    "orientation": float    # radians
  }
}
```

**Output (Navigation Result):**
```python
{
  "status": str,  # "succeeded" | "failed" | "cancelled" | "timeout"
  "final_pose": {
    "position": [float, float, float],
    "orientation": [float, float, float, float]
  },
  "path_length": float,     # meters
  "execution_time": float,  # seconds
  "failure_reason": Optional[str]
}
```

**Error Handling:**
| Error Type | Condition | User Impact | Recovery Strategy |
|------------|-----------|-------------|-------------------|
| `NoPathFound` | No collision-free path exists | Navigation fails | Adjust goal pose or clear obstacles |
| `PathBlocked` | Dynamic obstacle blocks planned path | Re-planning triggered | Wait for obstacle to clear or find alternate path |
| `ControllerFailure` | Robot cannot follow path | Navigation aborts | Reset robot state, retry with different parameters |

---

## Non-Functional Requirements (NFRs)

### Performance

- **Page Load Latency:** p95 < 3s on simulated 3G connection (1.6 Mbps, 150ms latency)
- **Lighthouse Performance Score:** > 90 for all documentation pages
- **Resource Budget:** Total page weight < 2MB (excluding videos, which are lazy-loaded)
- **Simulation Startup:** Docker container to running Gazebo < 10 minutes (including image pull)

### Reliability

- **Code Example Success Rate:** > 95% (tested in CI on each commit)
- **Link Validity:** 100% of internal links valid, external links checked weekly
- **Docker Image Availability:** 99.9% uptime (hosted on Docker Hub free tier)

### Security

- **API Key Handling:** Environment variables only, never committed to Git
- **Dependency Scanning:** Weekly automated scans (Dependabot, npm audit)
- **No PII Collection:** No analytics beyond aggregate page views (privacy-respecting analytics)

### Accessibility

- **WCAG Level:** AA compliance (automated + manual testing)
- **Screen Reader Compatibility:** NVDA (Windows) and VoiceOver (macOS) tested
- **Keyboard Navigation:** All interactive elements accessible via keyboard
- **Color Contrast:** 4.5:1 for normal text, 3:1 for large text
- **Video Captions:** All videos include accurate SRT captions
- **Diagram Alt Text:** All diagrams have descriptive alt text (50-150 words)

### Cost

- **Infrastructure:** $0/month (Vercel free tier for hosting, Docker Hub free tier)
- **LLM API Costs:** Documented for learners (est. $0.10-0.50 per capstone run with GPT-4)
- **Maintenance Effort:** ~2 hours/week (dependency updates, issue triage)

---

## Data Management

### Source of Truth

- **Content:** Git repository (`docs/module-4-vla/*.md`)
- **Configuration:** `docusaurus.config.ts`, `sidebars.ts`
- **Code Examples:** `docs/module-4-vla/code-examples/` (versioned with docs)
- **Assets:** `docs/module-4-vla/assets/` (diagrams, videos, images)
- **Dependencies:** `package.json` (Docusaurus), `requirements.txt` (Python)

### Schema Evolution

- **Content Structure:** Markdown frontmatter for metadata (backward compatible)
- **Code Interfaces:** Versioned JSON schemas for LLM output, detection results
- **Breaking Changes:** Major version bump in constitution, migration guide provided

### Migration & Rollback

- **Migration Path:** Git tags for each module release (v1.0, v1.1, etc.)
- **Rollback Plan:** Git revert to previous tag, redeploy (5-10 minutes)
- **Data Retention:** All versions preserved in Git history indefinitely

---

## Operational Readiness

### Observability

**Logs:**
- Docusaurus build logs (CI artifacts)
- Code test execution logs (pytest output)
- Accessibility scan results (axe-core JSON reports)

**Metrics:**
- Page views per section (privacy-respecting analytics)
- Lighthouse scores tracked over time
- Docker image pull counts

**Traces:**
- Not applicable (static documentation site)

### Alerting

| Alert | Threshold | Severity | On-Call Owner |
|-------|-----------|----------|---------------|
| Build Failure | Any CI build fails | P2 | Content maintainer |
| Broken Links | > 5 external links broken | P3 | Content maintainer |
| Performance Regression | Lighthouse score < 85 | P3 | Content maintainer |
| Accessibility Violation | Any WCAG AA failure | P2 | Content maintainer |

### Runbooks

- [ ] Deployment procedure: Git push to main → Vercel auto-deploy
- [ ] Rollback procedure: Git revert → push (triggers redeploy)
- [ ] Troubleshooting guide: Added to `docs/module-4-vla/10-debugging.md`
- [ ] Dependency update procedure: Renovate bot PRs, test in CI, merge

### Deployment Strategy

- **Environment Progression:** Local dev → PR preview (Vercel) → Production (main branch)
- **Rollout Strategy:** Direct deployment (educational content, low risk)
- **Feature Flags:** Not applicable (content is atomic)
- **Backward Compatibility:** Old links redirect, deprecation notices for changed content

---

## Risk Analysis & Mitigation

### Top Risks

**Risk 1: Simulation Setup Complexity Deters Learners**
- **Impact:** High (directly affects completion rate success metric)
- **Probability:** Medium (ROS 2 setup is notoriously complex)
- **Blast Radius:** All learners attempting capstone project
- **Mitigation:**
  - Docker container with pre-configured environment (target <10 min setup)
  - Video walkthrough of container setup process
  - Detailed troubleshooting guide for common Docker issues
  - Alternative: manual installation guide for "deep dive" learners
- **Kill Switch:** Provide cloud-based simulation alternative if Docker adoption < 50%

**Risk 2: LLM Output Variability Causes Inconsistent Task Plans**
- **Impact:** Medium (affects learning experience, debugging frustration)
- **Probability:** High (LLMs are non-deterministic)
- **Blast Radius:** Section 4 (LLM Planning) and Section 9 (Capstone)
- **Mitigation:**
  - JSON schema validation (reject invalid plans immediately)
  - Temperature=0 for reproducibility in examples
  - Retry logic with exponential backoff (3 attempts)
  - Fallback: pre-generated example plans for offline testing
- **Kill Switch:** Switch to deterministic rule-based parser if LLM failure rate > 20%

**Risk 3: Speech Recognition Accuracy Varies Across Accents/Environments**
- **Impact:** Medium (frustrating for some learners)
- **Probability:** Medium (Whisper is robust but not perfect)
- **Blast Radius:** Section 2 (Voice-to-Action) and Section 9 (Capstone)
- **Mitigation:**
  - Document noise handling best practices
  - Provide text-based command fallback interface
  - Test with diverse audio samples (different accents, noise levels)
  - Use Whisper's language-specific models if needed
- **Kill Switch:** Default to text input if speech recognition satisfaction < 3.0/5.0

---

## Validation & Testing

### Definition of Done

- [ ] All unit tests pass (pytest coverage > 80%)
- [ ] Integration tests pass (end-to-end capstone execution)
- [ ] Accessibility audit passes (axe-core: 0 violations, pa11y: 0 errors)
- [ ] Security scan clean (npm audit: 0 high/critical vulnerabilities)
- [ ] Performance benchmarks met (Lighthouse > 90, <3s load on 3G)
- [ ] All documentation sections complete with exercises
- [ ] Code review approved by technical SME
- [ ] Manual walkthrough by external reviewer (non-author)

### Test Strategy

**Unit Tests (pytest):**
- Coverage target: 80% of code-examples/ scripts
- Critical paths:
  - LLM planner: JSON schema validation, retry logic
  - Object detector: 3D pose estimation accuracy
  - Navigation client: Error handling, timeout management

**Integration Tests:**
- Scenarios:
  1. Voice → Text → LLM Plan → Validation
  2. LLM Plan → ROS Actions → Execution
  3. Object Detection → Grasp Pose → Manipulation
  4. Full pipeline: Voice command → Object manipulation
- Execution: In Docker container (simulates learner environment)

**Accessibility Tests:**
- Tools: axe-core (automated), pa11y-ci (CLI), manual keyboard testing
- Browsers: Chrome, Firefox, Safari, Edge
- Screen readers: NVDA (Windows), VoiceOver (macOS)
- Manual checklist:
  - [ ] All images have alt text
  - [ ] All videos have captions
  - [ ] Keyboard navigation functional
  - [ ] Focus indicators visible
  - [ ] Color contrast meets 4.5:1

**Performance Tests:**
- Lighthouse CI configured in GitHub Actions
- Budget:
  - Performance > 90
  - Accessibility > 95
  - Best Practices > 90
  - SEO > 90
- Network throttling: 3G simulation (1.6 Mbps, 150ms latency)

**Visual Regression:**
- Tool: Manual screenshot comparison (low-risk static content)
- Critical pages:
  - Module index
  - Section 9 (capstone)
  - Code example embeds

---

## Constitution Alignment

✅ **Educational Excellence:**
- Progressive complexity: individual components → integrated system
- Hands-on exercises in every section (2-8) + capstone project (9)
- Clear learning objectives stated upfront
- Debugging guidance (Section 10) teaches troubleshooting

✅ **Technical Accuracy:**
- All code examples tested in CI pipeline before merge
- References to official documentation (ROS 2, Whisper, YOLOv8)
- Validated against ROS 2 Humble LTS (supported until 2027)
- Technical review by SME required for content approval

✅ **Accessibility First:**
- WCAG 2.1 AA compliance enforced by automated tests
- Video captions and transcripts for all demos
- Keyboard-navigable tutorials and code examples
- Alt text on all diagrams with architectural descriptions
- Responsive design tested on mobile, tablet, desktop

✅ **Maintainability & Scalability:**
- Modular content structure (10 independent sections)
- Reusable code components (importable Python modules)
- Docusaurus conventions followed (clear file organization)
- Automated dependency updates (Renovate bot)

✅ **Security & Privacy:**
- No PII collection (privacy-respecting analytics only)
- Audio processing documented as local-first (Whisper runs locally)
- API keys in environment variables, never committed
- Weekly dependency vulnerability scans

✅ **Open Source Collaboration:**
- Full codebase on GitHub (MIT license)
- Contributing guide in repository
- Issue templates for bug reports and feature requests

✅ **Performance & Efficiency:**
- Images optimized (WebP/AVIF, < 100KB each)
- Videos compressed (< 5MB/min, lazy-loaded)
- Lighthouse Performance > 90
- <3s page load on 3G (NFR-2 from spec)

✅ **Version Control & Deployment:**
- All changes via Git (conventional commits)
- CI/CD validates before deployment
- Main branch always deployable (protected)
- Automated deployment on merge (Vercel)

---

## Architectural Decision Records (ADRs)

Significant decisions documented in separate ADRs:

- [ ] ADR-001: LLM Provider Selection (GPT-4 vs. Local Models) - `history/adr/001-llm-provider-selection.md`
- [ ] ADR-002: Simulation Delivery via Docker - `history/adr/002-docker-simulation-environment.md`
- [ ] ADR-003: Hybrid Code Format (Notebooks + Scripts) - `history/adr/003-hybrid-code-format.md`
- [ ] ADR-004: Object Detection Model (YOLOv8n) - `history/adr/004-object-detection-model.md`

**ADR Creation Trigger:**
These decisions meet the significance criteria:
- **Impact:** Long-term consequences (LLM lock-in, container dependency, code format affects all examples)
- **Alternatives:** Multiple viable options considered with documented trade-offs
- **Scope:** Cross-cutting (affects multiple sections, learner experience, CI pipeline)

**Recommendation:** Create ADRs after plan approval, before Phase 1 implementation.

---

## Timeline & Milestones

### Milestone 1: Infrastructure Ready
**Deliverables:**
- Docker container functional (ROS 2 + Gazebo)
- CI pipeline operational (lint, test, build)
- Project structure established

**Dependencies:** None

### Milestone 2: Components Functional
**Deliverables:**
- All 6 VLA components working (voice, LLM, vision, nav, manipulation)
- Jupyter notebooks for Sections 2-8
- Unit tests passing

**Dependencies:** Milestone 1 complete

### Milestone 3: Capstone Integrated
**Deliverables:**
- Full pipeline script (`full_pipeline.py`)
- Integration tests passing
- Demo video recorded

**Dependencies:** Milestone 2 complete

### Milestone 4: Content Complete
**Deliverables:**
- All 10 documentation sections written
- Diagrams and videos created
- Accessibility audit passing

**Dependencies:** Milestone 3 complete

### Milestone 5: Launch Ready
**Deliverables:**
- All quality gates passing
- External review complete
- Deployment successful

**Dependencies:** Milestone 4 complete

---

## Follow-Up Items

- [ ] Create ADRs for 4 key architectural decisions (estimated 2-3 hours)
- [ ] Set up Renovate bot for automated dependency PRs (estimated 1 hour)
- [ ] Record demo videos after capstone implementation (Milestone 3) (estimated 4-6 hours)
- [ ] Conduct external learner beta test after Milestone 4 (estimated 1 week)
- [ ] Establish baseline metrics tracking dashboard (post-launch) (estimated 2-3 hours)

---

**Constitution Check:** ✅ Aligned with v1.0.0
**Review Status:** DRAFT
**Last Updated:** 2025-12-07
