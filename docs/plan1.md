# Context

## Orchestrator – Project Summary

This project is a **batch Spark job orchestrator** designed to execute both **one-time and recurring workloads** under flexible scheduling constraints, with a strong focus on **optimization under uncertainty** (carbon intensity, Spot availability, and runtime variability).

### Core Concept

Instead of users choosing exact execution times, each workload occurrence is defined by:

- a fixed **anchor time** (when execution becomes allowed), and
- a hard **deadline** (by which execution must complete).

The time between anchor and deadline forms a **slack window**.

Within this slack window, the orchestrator—not the user—decides **when the job should actually run**.

This allows the system to:

- dynamically optimize execution timing
- reschedule jobs as better opportunities arise
- still guarantee deadline constraints

---

## Planning Model

Forecasts for carbon intensity and Spot availability are only reliable over a **short horizon** (e.g. ~48 hours). Because of this:

- Workload occurrences remain **UNPLANNED** until their entire slack window is covered by the forecast horizon.
- Only once sufficient forecast data exists does the orchestrator create an execution **plan** with a concrete start time.
- Plans may be **rescheduled** if forecasts improve, until execution starts or the plan is explicitly locked.

Execution plans are treated as **tentative decisions**, with full history preserved for inspection and analysis.

---

## Optimization & Scheduling

Scheduling decisions are based on:

- **Carbon Intensity (CI)** forecasts
- **Spot Placement Score (SPS)** forecasts (derived from SARIMA models stored in S3)
- **Runtime estimates** learned from historical runs of the same app artifact on the same hardware, optionally conditioned on data characteristics
- **User preferences**, primarily a **Risk Mode** (Optimistic / Neutral / Conservative)

A standalone **Scheduling Algorithm Module** performs Pareto-style optimization over feasible start times.

An **Execution Window Planner Service** orchestrates runtime estimation, forecast evaluation, and algorithm invocation, returning a suggested start time and decision metadata.

---

## Rescheduling & Stability

A periodic **Planning + Reschedule Service**:

- plans new occurrences when eligible
- re-evaluates existing plans as forecasts change
- applies rescheduling only when improvements are meaningful
- freezes plans near execution or when user-locked

To avoid thrashing, the system can delay planning until sufficient forecast coverage exists and applies thresholds when rescheduling.

---

## Explainability & Retrospection

At key moments (anchor time, plan creation, reschedule), the orchestrator captures **forecast snapshots** (stored in S3 and referenced in the database). This enables:

- post-run analysis
- “what-if” simulations under different risk modes
- comparison against baseline strategies (e.g. execute immediately at anchor)

All plans and reschedules are preserved as immutable history.

---

## Execution Model

Jobs are executed as **ephemeral EMR clusters** launched dynamically via AWS APIs.

Long-lived infrastructure (IAM roles, S3 buckets, networking) is created once per tenant using a **CloudFormation account-linking stack**.

The orchestrator:

- never stores long-lived AWS credentials
- assumes customer-owned IAM roles using STS + External ID
- keeps execution infrastructure fully isolated per tenant

---

## Client & Authentication Model

The system is exposed via a **web application** backed by a public API.

Authentication is intentionally lightweight:

- tenants are created manually (research project)
- each tenant receives an **API key**
- the web UI uses the API key as its authentication mechanism

---

## Persistence & Data Model

The orchestrator maintains persistent state for:

- tenants and AWS account links
- application artifacts
- workload definitions
- occurrences (anchor/deadline windows)
- execution plans and reschedule history
- forecast snapshots
- actual execution runs

Runtime history is stored on completed runs and reused to improve future scheduling decisions.

---

## Design Philosophy

- **Decouple intent from execution**
- **Plan late, reschedule opportunistically**
- **Optimize under uncertainty, not determinism**
- **Prefer explainability over black-box scheduling**
- **Keep client interactions simple; centralize intelligence server-side**

# Public API Layer

- Purpose: talks to the web app.

## Forecast Sources

- Orchestrator should be the source of:
    - Carbon Intensity forecasts
    - Spot Fleet forecasts

## Scheduling Algorithm API

# Configuration

- The orchestrator requires configuration to ensure it has access to the required data sources / APIs.

# Client Account Linking

## Account Linking CloudFormation Stack

- Resources:
    - IAM Role
        - Must be created and then trusted by the AWS Orchestrator account.
        - Used for launching and managing clusters from the Orchestrator on the client’s account, as well as being able to read / write data from the S3 buckets on the client’s account.
    - S3 Buckets
        - Input bucket creation
        - Output bucket creation
        - Logs bucket creation
- The stack should output back to the Orchestrator / Client:
    - IAM Role ARN
    - Input bucket ARN
    - Output bucket ARN

## Client Parameters

- Input / Output / Log Bucket Names
- IAM role name
- Subnet choice

## Client IAM Role Verification

- quick note: used to ensure that the stack creation was successful - in terms of that the orchestrator can assume the IAM role and that buckets can be accessed.

## Infrastructure Deletion

# CloudFormation Templates

## Subnet

# Security and Authentication

## Adding New Users

- On the Orchestrator server, we can run an “add new tenant” script.
- Process:
    - Create a new tenant entry in the DB. Script takes a name on runtime.
    - Generate an API key. Show once on creation, and then store the hash in the tenant entry.

## Client Authentication

- On the client site, the Authentication page will have an Enter API Key section. Once entered, the tenant will essentially be logged in.

## Tenant IAM Isolation

# Orchestrator Database

## tenants Table

- Columns:
    - tenant_id (PK)
    - name
    - created_at
    - api_key_hash

## aws_links Table

- Columns:
    - aws_link_id (PK)
    - tenant_id (FK to tenants Table)
    - role_arn
    - input_bucket
    - output_bucket
    - logs_bucket
    - external_id
    - stack_name
    - created_at
    - last_verified_at (nullable)

## app_artifacts Table

- Contains metadata pointing to the app.zip stored in the orchestrator S3 bucket
- Columns:
    - artifact_id (PK)
    - tenant_id (FK)
    - artifact_hash
    - s3_uri
    - created_at

## workloads Table

- The user’s workload definition. This is the “template” from which occurrences come from.
- Note that there are no data S3 paths. Instead, the input / output paths are specified in the aws_links table, created when they run the CloudFormation template. Instead, the system will write data to: bucket_name/workload-name+id/…
- Columns:
    - workload_id (PK)
        - Primary key. A unique ID representing this workload.
    - tenant_id (FK)
        - Foreign key representing the owner of this workload.
    - name
    - description
    - tags_json
        - User can associate tags with a workload for UX purposes. Perhaps could support filtering by tags on the client UI, so people could group workloads by projects for example.
        - Optional
        - JSON array
    - artifact_id (FK)
        - Foreign key to the app_artifacts table.
    - schedule_rules_json
        - Anchor time rule (e.g. daily at 5pm, every Wednesday at 9AM, etc)
        - Deadline rule (e.g. relative from anchor time, absolute deadline)
        - Recurrence rules (e.g. will this workload repeat, and when)
    - fleet_template_id (FK)
        - Foreign key to the Fleets table.
        - Represents the EMR cluster and hardware the workload will use.
    - user_preferences_json
        - Risk Modes
        - Preference weighting
    - manual_runtime_seconds (nullable)
    - is_active
        - Allow users to disable this workload from running / creating occurrences without fully removing it
    - created_at
    - updated_at
        - In case we add the ability to change workload settings later

## occurrences Table

- An occurrence is a concrete run window from a workload. Occurrences are what the planner + scheduler act upon.
- Columns:
    - occurrence_id (PK)
    - workload_id (FK)
        - Foreign key to the workload used to generate this occurrence.
    - anchor_time (datetime)
        - Represents the time generated by the workload schedule rules as to when this workload must consider starting.
    - deadline_time (datetime)
        - Represents the hard deadline of the job from the anchor time.
    - state (ENUM)
        - UNPLANNED - run window is outside the forecast horizon, we cannot optimise properly for an execution time just yet.
        - SCHEDULED - an execution plan has been created for the job, and it is scheduled to be run. The plan itself may still be rescheduled to another time UNLESS the occurrence is locked.
        - RUNNING - execution has now started for this occurrence. The plan is locked and cannot be changed. Infrastructure has been launched and the job should be executing.
        - SUCCEEDED - the job for this occurrence completed successfully. Outputs should be available at the configured destination.
        - FAILED - execution was attempted but did not complete successfully.
        - CANCELLED - the occurrence was explicitly cancelled.
    - locked
        - Boolean value.
        - Represents if the user has decided they are satisfied with the plan, and do not want it to be rescheduled further.
    - current_plan_id (nullable FK to plans table)
    - created_at
    - updated_at
- Notes:
    - current_plan_id points to the most recent plan for an occurrence, since we can have many plans if rescheduled.

## occurence_snapshots Table

- For a given occurrence, we may capture multiple forecast snapshots at different moments. For example, we could capture forecast snapshots at the anchor time (for baseline execution lookback), when we rescheduled, when we actually started. Each snapshot is a row that points to an S3 object.
- Columns:
    - snapshot_id (PK)
    - occurrence_id (FK)
    - snapshot_type (ENUM)
        - AT_ANCHOR
            - snapshot of the forecasted values at the anchor time, so we can use this as a “baseline” execution value
        - AT_PLAN_CREATED
            - forecast values that were use to decide the plan
    - plan_id (nullable FK)
    - s3_uri (where the forecast blob lives)

## plans Table

- The chosen execution plan for an occurrence.
- Columns:
    - plan_id (PK)
    - occurrence_id (FK)
    - status (ENUM)
        - ACTIVE - the current active plan for an occurrence
        - SUPERSEDED - this plan is no longer active as a reschedule as occurred
        - CANCELED
    - planned_start_time
    - created_at
        - The time at which the plan was created.
- One occurrence can have many plans, since we can reschedule if better conditions occur. This means the plan tables can essentially act as a reschedule history too.

## runs Table

- The real execution record (what actually happened)
- Columns:
    - run_id (PK)
    - occurrence_id (FK)
    - status (ENUM)
        - QUEUED, PROVISIONING, RUNNING, SUCCEEDED, FAILED, CANCELLED
    - emr_cluster_id (optional)
    - started_at
    - finished_at
    - error_summary (nullable text)
    - artifact_id (FK, app_artifacts Table)
    - fleet_template_id (FK, fleets Table)
    - runtime_seconds
    - data_features_json
        - IMPORTANT: Our runtime prediction model uses historical runs of an app artifact on certain hardware, and depends on the data. We need to be able to store characteristics of the data for a run so we can create our model.

## fleet Table

# Forecast Outputs Module

# Runtime Prediction Module

## Required Data for Model

- Run Identity -
    - job name / version
- Cluster hardware
- Spark config
- Input data descriptors. For each main input:
    - total bytes read
    - row count
    - file count + avg file size
    - format
- Spark event-log derived stage metrics
    - runtime
    - shuffle read bytes + shuffle write bytes
    - spilled bytes
    - GC time
    - task distribution time
    - input bytes read per stage
    - records read/written
- Skew indicators
    - max partition size / median partition size
    - top-k largest shuffle partitions
- S3 Infrastructure Signals
    - S3 bytes read/written
    - Network throughput

## How to Collect the Metrics

- During execution:
    1. Enable Spark event logging to S3 (per run path)

## Metrics Store

- Metrics for a run will be stored in an S3 bucket, and a run entry in the DB will store the link to the logs.

# Scheduling Algorithm Module

## Inputs

- S3 URI to the SPS SARIMA forecasting model
- Carbon Intensity forecast (time series)
- Deadline (Datetime)
- Risk Mode (ENUM - Neutral / Conservative / Optimistic)
- Job runtime estimation

## Outputs

- 

# Execution Window Planner Service

## Purpose

- The Execution Window Planner Service is the service that generates the optimal start time of a job, given the conditions.
- It is used by the Orchestrator’s Planning + Reschedule Service.

## Inputs

- Occurrence anchor time
- Occurrence deadline
- S3 URI of forecast model for fleet spot instances
- Runtime history of previous occurrences of that workload
- User preferences for the workload

## Process

1. Calls the Runtime Prediction Module to receive an estimate of the job’s runtime, required for selecting the appropriate start time
2. Calls the Scheduling Algorithm Module

## Outputs

- Forecast Output Values
    - Carbon Intensity forecast
    - SPS Forecast (modified by Risk Mode)
- Job runtime estimate (modified by Risk Mode)
- Suggested start time

# New Workload Service

## Purpose

- Accept a workload submission from the web app and persist everything required for the orchestrator to:
    - generate occurrences over time
    - plan / schedule within forecast horizon later
    - execute runs in the customer’s AWS account

## Inputs (from Client App)

- Tenant identity (from API Key we can get tenant_id)
- Workload metadata (name, description, tags)
- App artifact selection (likely a ZIP file submitted from app)
- Schedule rules (anchor pattern + deadline rule + recurrence)
- Fleet selection (fleet_template_id)
- Preferences (risk mode, weights, potentially more)
- Manual runtime estimate (maybe)

## High Level Steps

1. Authenticate + validate ownership
    - Resolve tenant id from API key
2. Validate workload definition
    - Validate schedule rules are well-formed:
        - anchor rule
        - deadline rule
        - timezone handling
    - Validate “can we ever meet deadlines”
        - e.g. deadline after anchor, slack > 0
    - Validate app artifact is usable
        - TODO: how?
3. Persist Workload Record in DB
4. Generate initial occurrences

# Planning Service

## Purpose

- The Planning is responsible for:
    - deciding when a job should be planned
    - choosing when it should run within its slack window
    - rescheduling existing plans as forecasts change
    - persisting plans and forecasts snapshots for later inspection
- Benefits of this is that we can reschedule if new opportunities arise.
- Furthermore, as we use data reference links, runtime estimation for the jobs will become more accurate as it gets closer to the anchor time, given that data patterns may change at the link.

## When It Runs

- The service runs on a fixed cadence (every 30 minutes), matching the coarsest forecast update interval.

## High Level Loop

- On each run, the service performs the following steps:
1. Load latest forecasts
    - Carbon intensity (CI)
    - Spot Placement Scores (SPS)
2. Select candidate occurrences
    - PLANNED occurrences - no execution plan exists yet
    - SCHEDULED occurrences -
        - Have a plan, but:
            - have not started execution, and
            - are not locked or inside the freeze window

## Planning New Occurrences (PLANNED → SCHEDULED)

- For each PLANNED occurrence:
1. Check forecast horizon coverage
    - If the entire slack window [anchor, deadline] is covered by available CI and SPS forecasts, the occurrence is eligible for planning.
        - Justification for this is because if we instead only wait until the estimated runtime is covered by the forecast horizon, then the scheduler will of course choose that time. As new forecast values come in, the scheduler is likely to just choose them each time the rescheduling event occurs, which means constant replans.
        - Alternative options involve setting a minimum forecast coverage of the slack window before starting planning. This could either be a client decided option, or set by the orchestrator.
        - A downside of the method though is that if the forecast horizon is relatively short (e.g. 48 hours), then we start planning pretty late.
    - Otherwise:
        - leave it PLANNED
2. Run Execution Window Planner Service
3. Capture plan-time forecast snapshot
    - Store the forecasts used in the scheduling algorithm during plan-time in the occurrence-snapshots table, for possible use in later analysis.
4. Create plan
    - Persist a new ACTIVE plan
    - Set occurrence.state to SCHEDULED

## Rescheduling Existing Plans (SCHEDULED → SCHEDULED)

- For each SCHEDULED occurrence:
1. Check rescheduling eligibility
    - Skip if:
        - execution has started
        - rescheduling policy is LOCK
        - too close to existing plan scheduled start time (decide on threshold?)
        - wouldn’t have time to reschedule anymore based on predicted runtime (what if we have no predicted runtime?)
2. Run Scheduling Algorithm Module with updated forecast values, using runtime prediction
3. Capture reschedule-time snapshot
    - Store forecasts used for this re-evaluation in S3
4. Compare with current plan
    - If execution window has “better” average values for carbon intensity / better entry SPS, then accept the plan, using a threshold. OR pareto domination?
5. Update Plan History
    - Mark previous ACTIVE plan as SUPERSEDED
    - Insert new plan as ACTIVE
    - Update occurrence.current_plan_id

## Snapshot Strategy

- The service captures forecast snapshots at key moment, for the purposes of later analysis.
    - AT_ANCHOR - when the occurrence anchor time is reached
    - AT_PLAN_TIME - when plan is first created. allows us to see what forecasts the system was using.

# Execution Engine

- Purpose?
    - Takes the scheduled plan and begins to launch the infrastructure / run the jobs / collect the metrics

## Purpose

- Execute a planned occurrence by:
    - assuming the tenant’s IAM role
    - provisioning the required EMR cluster in the tenants AWS account
    - running the Spark application for the selected app artifact + workload inputs
    - collecting execution metadata, logs, and runtime/metrics signals
    - tearing down infrastructure reliabily
- Provide a clean boundary between:
    - “decide when to run it” (planner)
    - “actually run it”

## High Level Loop

1. Loop through all 

## CloudFormation Stack

## Capturing Forecast Actuals after Run

# Observability

# Orchestrator S3 Buckets

## orchestrator-artifacts

- tenants/{tenant_id}/artifacts/{artifact_hash}/
    - app.zip

## orchestrator-snapshots

- tenants/{tenant_id}/occurrences/{occurrence_id}/snapshots/
    - forecasts/
        - AT_ANCHOR
        - AT_PLAN_TIME
    - actuals/
        - ANCHOR_DEADLINE_WINDOW
            - forecast actuals from the slack window
        - STARTTIME_ENDTIME_WINDOW
            - forecast actuals from the execution period

## orchestrator-logs

- tenants/{tenant_id}/runs/{run_id}/
    - …

# Orchestrator Infrastructure

Run on an EC2 instance on AWS

## Always-On

- API
- Execution Engine

## Periodic / Worker

- Planning service