# Essential terms

## Foundations

| Term | Meaning and example |
|---|---|
| **Process** | A running instance of a program, with an identity, permissions and resources. Taskboard's process can be alive while its database connection is broken. |
| **Port and socket** | A port identifies a network endpoint on a machine; a socket is an operating-system communication endpoint. Two servers normally cannot bind the same address and port. |
| **DNS** | The system that resolves names into records, including IP addresses. Successful DNS resolution proves neither that a server accepts connections nor that its application works. |
| **TCP** | A transport protocol providing an ordered byte stream with delivery mechanisms. A successful TCP connection says nothing about whether Taskboard returns the correct task. |
| **TLS** | Protects a connection's confidentiality and integrity and can authenticate endpoints through certificates. A certificate must match the expected identity and a trusted verification chain. |
| **HTTP** | An application protocol using requests and responses, including methods, status codes and headers. HTTP 200 with incorrect task data is still an application failure. |
| **CIDR** | Notation describing an IP address range through a prefix length. `10.0.1.0/24` contains 256 IPv4 addresses; not all addresses are necessarily usable by workloads. |
| **Reverse proxy** | Receives client requests and forwards them to application servers. It may terminate TLS or balance traffic; its own timeout can fail an otherwise functioning request. |

## Building, testing and delivery

| Term | Meaning and example |
|---|---|
| **Git** | Records versioned changes and their history. A commit identifies a source revision; it does not, by itself, identify the dependencies or configuration used to build it. |
| **Continuous integration: CI** | Frequently integrating changes while automatically checking them. Taskboard's merge request runs meaningful tests; a pipeline containing only successful placeholder commands provides no useful assurance. |
| **Continuous delivery and deployment: CD** | Delivery keeps validated changes releasable; deployment also automates their release. A manual release decision can be part of continuous delivery without weakening automated testing. |
| **Pipeline** | An ordered or dependency-linked set of automated jobs. Taskboard's pipeline tests, builds, checks and deploys; each stage should have clear inputs, outputs and failure behavior. |
| **Runner** | The execution environment that performs CI jobs. Job code can use the runner's available permissions, files and credentials, so runner isolation is a security boundary. |
| **Image** | A packaged filesystem and metadata used to start containers. Adding a secret to an image and deleting it in a later layer can leave it recoverable. |
| **Container** | An isolated running process and its environment, commonly sharing a kernel with other containers. Restarting a container does not make its temporary filesystem durable storage. |
| **Digest** | A content-derived identifier for an artifact. Promote the tested image digest: a friendly tag such as `staging` can later point to different content. |
| **Registry** | Stores and distributes artifacts such as container images. Authentication controls access; storing an image there does not establish that its contents are trustworthy or tested. |
| **Cache** | Reusable material intended to speed up work, such as downloaded dependencies. A correct build should tolerate a missing cache; stale cache contents must not silently alter correctness. |
| **Artifact** | A declared output retained or transferred from a job, such as a test report or packaged application. Unlike a cache, downstream work may explicitly require it. |
| **Unit test** | Checks a small unit of behavior with its dependencies isolated where appropriate. Test title validation directly without starting PostgreSQL, Kubernetes or an HTTP server. |
| **Integration test** | Checks interaction across a real boundary between components. Creating and retrieving tasks through actual PostgreSQL can expose SQL and transaction defects that mocks miss. |
| **System test** | Checks the assembled system through its external behavior. Create, complete and retrieve a task through the deployed API, then verify persistence across an application restart. |
| **Mock** | A controlled stand-in for a dependency, configured to return particular behavior. A mock database can test error handling but cannot establish whether real SQL is valid. |
| **Migration** | A versioned change to stored data or its schema. Adding an optional column can preserve compatibility; removing a column may break the previous application during rollback. |
| **Idempotency** | Repeating an operation has the same intended effect as performing it once. An idempotency key can prevent a retried request from creating duplicate tasks. |

Test levels describe boundaries. Smoke checks cover essential behavior; performance and security describe purposes that can cross several levels.

## Cloud identity and infrastructure

| Term | Meaning and example |
|---|---|
| **IAM** | Identity and access management: mechanisms for identities, permissions and access decisions. Give the deployment identity permission for its environment instead of unrestricted account administration. |
| **Authentication** | Establishing the identity making a request. Validating a user's login or a workload's token answers who it is, not which actions it may perform. |
| **Authorization** | Deciding whether an identified caller may perform an action on a resource. A valid deployment identity can still be correctly denied access to another environment. |
| **Role** | A provider-specific way to organize permissions or assume an identity with permissions. AWS and GCP use this term differently; compare their actual identity and policy models. |
| **OIDC** | OpenID Connect, an identity protocol using verifiable tokens. GitLab can present job identity to a cloud; tightly checked claims can enable short-lived deployment access. |
| **Infrastructure as code: IaC** | Describing and managing infrastructure using versioned code or configuration. Terraform configuration becomes reviewable, but unsafe permissions remain unsafe when expressed neatly in code. |
| **Terraform state** | Terraform's record connecting configured resources to managed objects and attributes. It is not a backup of application data and may contain sensitive values. |
| **Drift** | Actual infrastructure differs from recorded or declared expectations. A manually opened firewall rule can create drift; investigate the difference before deciding which version should win. |

## Kubernetes

| Term | Meaning and example |
|---|---|
| **Pod** | Kubernetes' scheduling unit containing one or more closely related containers sharing networking and selected storage. A replacement Pod is a new instance, not the original process repaired. |
| **Deployment** | A controller-managed declaration for replicating and updating Pods through ReplicaSets. It helps maintain desired replicas; those replicas still need valid configuration and healthy dependencies. |
| **Service** | A stable access abstraction for selected backends, commonly Pods. A Service name can resolve successfully while no ready application endpoints are available behind it. |
| **Ingress** | A resource describing HTTP/HTTPS routing into services, implemented by an ingress controller. Creating the resource alone does not install or configure an external load balancer universally. |
| **Gateway API** | A family of resources separating infrastructure and routing responsibilities. A compatible implementation is required; defining an HTTPRoute alone does not create a functioning traffic path. |
| **RBAC** | Role-based access control for Kubernetes API operations. Permission to read Deployments does not imply permission to read Secrets, and neither directly controls application network traffic. |
| **NetworkPolicy** | Declares allowed network traffic for selected Pods. Enforcement depends on the networking implementation; validate that a forbidden connection actually fails rather than trusting the YAML alone. |
| **PersistentVolumeClaim: PVC** | A request for storage with specified characteristics, which can bind to a volume. Persistence across Pod replacement does not guarantee replication, backup or recovery from deletion. |
| **CNI** | Container Network Interface: a specification used by networking plugins to configure container networking. Plugin capabilities differ, including whether and how network policies are enforced. |
| **Requests and limits** | Requests inform scheduling and resource allocation; limits bound configured resource use. CPU limits can cause throttling, while exceeding a memory limit can lead to termination. |
| **Horizontal Pod Autoscaler: HPA** | Adjusts workload replica counts using configured metrics. Adding Taskboard replicas will not fix a saturated database and may increase pressure on it. |
| **Reconciliation** | Repeatedly observing actual state and attempting to bring it toward desired state. A controller may recreate a deleted Pod because the desired replica count still requires it. |
| **Probes** | Startup, readiness and liveness checks answer different questions. Readiness affects traffic eligibility; liveness can trigger restarts. A shared database outage usually should not restart every application. |

## Reliability and operations

| Term | Meaning and example |
|---|---|
| **Telemetry** | Measurements emitted by a system, including logs, metrics and traces. Correlating request IDs and timings helps explain an incident; collecting more data alone does not provide understanding. |
| **Service-level indicator: SLI** | A defined measurement of service behavior from a relevant perspective. For Taskboard, measure successful valid requests divided by eligible requests, with explicit exclusions. |
| **Service-level objective: SLO** | A target for an SLI over a defined window. Specify the measurement and workload; “fast and reliable” is too vague to evaluate. |
| **Service-level agreement: SLA** | An agreement about service commitments and consequences. An internal learning-lab SLO does not automatically become a customer contract or an entitlement to compensation. |
| **Error budget** | The tolerated shortfall implied by an SLO over its measurement window. Spending it quickly signals elevated risk and can guide release or reliability decisions. |
| **Recovery time objective: RTO** | The target time to restore an acceptable service after disruption. A 30-minute target must be tested against measured recovery, including configuration and data restoration. |
| **Recovery point objective: RPO** | The target maximum tolerable data loss measured in time. Daily backups may imply substantial loss; the latest successful, usable recovery point matters more than the schedule. |
| **Throughput** | Work completed per unit of time under stated conditions. Record completed requests per second alongside latency and failures; sending many requests is not proof of completing them. |
| **p95** | The 95th percentile of a defined set of measurements. A p95 request latency of 200 milliseconds means approximately 95% of measured requests completed within that time. |
| **Latency** | Time taken for an operation, measured between stated boundaries. Client-observed latency includes delays that an application's internal handler timer may omit, such as network or queueing time. |
| **Availability** | How often a service meets a defined usable condition. Running processes do not establish availability if users cannot successfully create or retrieve their tasks. |
| **Rollback** | Returning a deployment to a previous known version or configuration. Application rollback may fail after an incompatible schema change; data recovery is a separate decision. |

