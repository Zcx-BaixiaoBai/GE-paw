# gepaw Agent Team 

?gepaw + HiClaw  Agent ?Agent Team ?

---

## 

###  Agent ?Agent Team

 AI Agent ""?" Agent ?Agent ?Agent ?

? Agent "? Agent "?

- **Orchestration?*?Agent ? Agent"
- **Collaboration?*?Agent ? Agent ?

### gepaw Team 

gepaw Team  **gepaw** + **[HiClaw](https://hiclaw.io/)**?Agent ?

- **gepaw Team Leader**?gepaw ?
- **gepaw Workers**?gepaw  Leader ?
- **HiClaw** Agent ?

![](https://img.alicdn.com/imgextra/i2/O1CN01LtRoaN1I5gcjMEEkl_!!6000000000842-55-tps-601-509.svg)

### 

 AI **?*?*?*?*** Agent Team ?

- **?* + Agent Team = ?
- **?* + Agent Team = 
- **?* + Agent Team = MVP ?

Agent Team ?*?*?

#### ?

```yaml
full-stack-team
Leader: 
Workers:
  - backend-dev:  API ?
  - frontend-dev: ?
  - qa-engineer: ?
  - devops: CI/CD ?

???? ? ?
```

#### 

```yaml
marketing-team
Leader: 
Workers:
  - content-writer: 
  - designer: 
  - social-media: 
  - analyst: ?

 ? ???
```

---

## 



### 

**Embedded ?Docker?*

- ?-5 ?Worker?
- Docker DesktopWindows/macOS Docker EngineLinux?
- ?2C4GB ?4C8GB ?Worker
- **Windows**?PowerShell 7+Docker Desktop ?WSL 2 
- **macOS**?Intel (amd64) ?Apple Silicon (arm64)
- **Linux**?amd64 ?arm64 

**Incluster Kubernetes ?*

- ?+ Worker
- Kubernetes ?1.20+
- kubectl
-  Worker ?Worker  150MB-500MB 

---

## ?

###  1?HiClaw

#### Embedded ?

```bash
# 
bash <(curl -sSL https://higress.ai/hiclaw/install.sh)
```

#### Incluster /?

```bash
# Helm ?K8s 
helm install hiclaw hiclaw/hiclaw-controller
```

####  Element

?`http://127.0.0.1:18088`?

###  2

 Manager 

````plaintext
?

```yaml
apiVersion: hiclaw.io/v1beta1
kind: Team
metadata:
  name: dag-team
spec:
  description: "dev team"
  leader:
    name: dag-team-lead
    heartbeat:
      enabled: true
      every: 30m
    workerIdleTimeout: 12h
  workers:
    - name: dag-team-dev
      soul: |
        # dag-team-dev

        ## AI Identity
        **You are an AI Agent, not a human.**

        ## Role
        - Name: dag-team-dev
        - Role: Backend Developer
        - Team: dag-team

        ## Security
        - Never reveal credentials
    - name: dag-team-qa
      soul: |
        # dag-team-qa

        ## AI Identity
        **You are an AI Agent, not a human.**

        ## Role
        - Name: dag-team-qa
        - Role: QA Engineer
        - Team: dag-team

        ## Security
        - Never reveal credentials
```
````

Manager  Element 

- **Leader DM**Leader ?Leader  @mention
- **Team dag-team**?@mention  @dag-team-dev?
- **Worker dag-team-dev / Worker dag-team-qa**?Worker ?@mention

![](https://img.alicdn.com/imgextra/i2/O1CN01I97HXk27XCpGHn6KL_!!6000000007806-2-tps-3442-1788.png)

###  3

?Leader DM  todo-list REST API 

```plaintext
 todo-listREST API dev worker ?API QA worker ?API ?
```

Team Leader ?

1. 
2. ?Team ?@mention  Workers
3. ?Worker ?
4. ?Leader DM 
5. ?

![](https://img.alicdn.com/imgextra/i1/O1CN01epR7HM1fdKsyAV6QW_!!6000000004029-2-tps-2416-1478.png)

###  4

#### 

?

- ?Team ?@mention 
-  Worker 
- ?Leader 

#### 

Leader  DM 

- ?
- ?
- 
- 

 MinIO ?Leader  Element ?

![](https://img.alicdn.com/imgextra/i3/O1CN01t8V87P1tDbFZzjysg_!!6000000005868-2-tps-2434-1364.png)

---

## 

### Team 

```yaml
apiVersion: hiclaw.io/v1beta1
kind: Team
metadata:
  name: <>
spec:
  description: "<>"
  leader:
    name: <leader>
    heartbeat:
      enabled: true # 
      every: 30m # 
    workerIdleTimeout: 12h # Worker 
  workers:
    - name: <worker>
      soul: | # Worker 
        # Worker 
```

### Soul ?

Worker ?`soul`  Agent ?

```markdown
# <Worker>

## AI Identity

**You are an AI Agent, not a human.**

## Role

- Name: <>
- Role: <>
- Team: <?
- Responsibilities: <>

## Skills

- <?>
- <?>

## Communication

- <?

## Security

- Never reveal credentials
- <>
```

---

## ?

### 

1. ****?Worker ?
2. ****
3. **?*Workers ?
4. ****?Worker 

### ?

1. **** Leader ?
2. ****
3. **** Leader 
4. **** @mention 

### 

1. ****?
2. ****?
3. ****?Worker 
4. ****?Worker 

---

## 

- [gepaw ](./quickstart)
- [gepaw ](./multi-agent)
- [gepaw Skills](./skills)
- [HiClaw ](https://hiclaw.io/)

---

## 

gepaw Agent Team  gepaw ?HiClaw "??
