# Tier Selection Guide

## Quick Decision Tree

```
Start here:
│
├─ How many main entities (data models)?
│  ├─ 1-5 entities → Likely TIER 1 (continue to check other factors)
│  ├─ 5-10 entities → Likely TIER 2 (continue to check other factors)
│  └─ 10+ entities → Likely TIER 3
│
├─ How many external system integrations?
│  ├─ None or 1 simple API → TIER 1
│  ├─ 2-4 APIs (payment, email, storage) → TIER 2
│  └─ 5+ systems (ERP, fiscal, payments, etc.) → TIER 3
│
├─ What's your scale/complexity?
│  ├─ Personal project, small team → TIER 1
│  ├─ Business application, startup → TIER 2
│  └─ Enterprise, multi-region, compliance → TIER 3
│
└─ Special requirements?
   ├─ None → TIER 1
   ├─ Auth, caching, some integrations → TIER 2
   └─ Compliance, HA, monitoring, message queues → TIER 3
```

## Scoring System

Answer these questions and add up your score:

### 1. Entity Count
- **1-3 entities**: 0 points
- **4-5 entities**: 1 point
- **6-10 entities**: 2 points
- **11+ entities**: 3 points

### 2. External Integrations
- **None**: 0 points
- **1 simple API** (e.g., just email): 0 points
- **2-3 APIs** (e.g., payment + email + storage): 1 point
- **4-5 systems**: 2 points
- **6+ systems** (ERP, CRM, fiscal, etc.): 3 points

### 3. Scale
- **Small**: Personal project or <100 users: 0 points
- **Medium**: Business app, 100-10,000 users: 1 point
- **Large**: Enterprise, 10,000+ users or multi-region: 2 points

### 4. Special Requirements
Count how many you need:
- Regulatory compliance (GDPR, HIPAA, fiscal): +2 points
- Multi-tenant: +1 point
- Real-time features (WebSocket, streaming): +1 point
- Message queues (Kafka, RabbitMQ): +2 points
- Advanced monitoring (distributed tracing): +1 point
- High availability (99.9%+ uptime): +1 point

### Total Score
- **0-2 points**: → **TIER 1** (Simple CRUD)
- **3-6 points**: → **TIER 2** (Standard REST API)
- **7+ points**: → **TIER 3** (Enterprise)

---

## Practical Examples

### TIER 1: Simple CRUD (0-2 points)

**When to use:**
- Building an MVP or prototype
- Personal project or internal tool
- Simple data management
- No external dependencies
- Quick turnaround needed (hours, not days)

**Examples:**
```
✅ TODO list app
✅ Personal blog
✅ Contact manager
✅ Bookmark collection
✅ Simple inventory tracker
✅ Team wiki
✅ Habit tracker
```

**What you get:**
- Basic CRUD operations
- Simple authentication (optional)
- PostgreSQL/MySQL database
- Docker for local dev
- Basic tests
- **Time: 30-45 minutes**

**What you DON'T get:**
- Complex integrations
- Caching layer
- Advanced monitoring
- Kubernetes deployment

---

### TIER 2: Standard REST API (3-6 points)

**When to use:**
- Building a real business application
- Need external integrations (payments, emails, cloud storage)
- Need proper authentication and authorization
- Performance matters (caching needed)
- Production deployment to cloud
- SaaS product or startup

**Examples:**
```
✅ E-commerce platform
   - Entities: User, Product, Order, Cart, Payment (5-8)
   - Integrations: Stripe, SendGrid, AWS S3 (3)
   - Score: 2 + 1 + 1 = 4 → TIER 2

✅ Project management tool
   - Entities: User, Project, Task, Team, Comment (5)
   - Integrations: Email, File storage, Calendar API (3)
   - Score: 1 + 1 + 1 = 3 → TIER 2

✅ Booking/Reservation system
   - Entities: User, Venue, Booking, Payment, Review (5-7)
   - Integrations: Payment gateway, Email, SMS (3)
   - Score: 2 + 1 + 1 = 4 → TIER 2

✅ Content management system (CMS)
   - Entities: User, Post, Media, Category, Comment (5-7)
   - Integrations: Cloud storage, Email, Search API (3)
   - Score: 2 + 1 + 1 = 4 → TIER 2
```

**What you get:**
- JWT authentication + RBAC
- External API integrations (2-4)
- Redis caching
- Rate limiting
- Comprehensive testing
- Security best practices
- Docker + cloud deployment
- **Time: 60-90 minutes**

**What you DON'T get:**
- Message queue infrastructure
- Advanced monitoring (distributed tracing)
- Kubernetes orchestration
- Complex compliance requirements

---

### TIER 3: Enterprise Application (7+ points)

**When to use:**
- Building an enterprise system
- Multiple complex integrations (5+)
- Regulatory compliance required
- Multi-region deployment
- High availability requirements (99.9%+)
- Complex business workflows
- Large scale (1000+ concurrent users)

**Examples:**
```
✅ POS (Point of Sale) System
   - Entities: 15+ (Transaction, Product, Customer, Store, etc.)
   - Integrations: 10+ (ERP, Payment, Fiscal, Loyalty, E-commerce, etc.)
   - Special: Fiscal compliance, Multi-region, HA
   - Score: 3 + 3 + 2 + 2 + 1 + 1 = 12 → TIER 3

✅ Healthcare Management System
   - Entities: 15+ (Patient, Appointment, Prescription, etc.)
   - Integrations: 8+ (Labs, Pharmacy, Insurance, etc.)
   - Special: HIPAA compliance, HL7 integration
   - Score: 3 + 3 + 2 + 2 = 10 → TIER 3

✅ Financial Trading Platform
   - Entities: 12+ (User, Account, Order, Position, etc.)
   - Integrations: 6+ (Market data, Banks, Clearing, etc.)
   - Special: Real-time, Compliance, HA
   - Score: 3 + 2 + 2 + 2 + 1 + 1 = 11 → TIER 3

✅ Supply Chain Management
   - Entities: 20+ (Product, Warehouse, Shipment, etc.)
   - Integrations: 10+ (Suppliers, Logistics, ERP, etc.)
   - Special: Multi-tenant, Real-time tracking
   - Score: 3 + 3 + 2 + 1 + 1 = 10 → TIER 3
```

**What you get:**
- Complete enterprise architecture
- 5+ external system integrations
- Message queue (Kafka/RabbitMQ)
- Multi-layer caching
- Distributed tracing
- Kubernetes deployment
- High availability setup
- Comprehensive monitoring
- Disaster recovery plan
- Compliance features
- **Time: 90-120 minutes**

---

## Red Flags: Don't Over-Engineer!

### ⚠️ You DON'T need TIER 3 if:
- ❌ "I might need it later" - **Start with TIER 1 or 2, upgrade when needed**
- ❌ "It sounds cool" - **Enterprise features add complexity**
- ❌ "Just in case" - **YAGNI (You Aren't Gonna Need It)**
- ❌ MVP or prototype - **Start simple, prove the concept first**

### ✅ Start with lower tier and upgrade when:
- You have **real users** experiencing performance issues
- You need to **integrate a new system** (upgrade TIER 1 → TIER 2)
- You have **regulatory requirements** (upgrade to TIER 3)
- You need **multi-region** deployment (upgrade to TIER 3)
- You have **concrete scaling needs** (not hypothetical)

---

## When to Upgrade Between Tiers

### TIER 1 → TIER 2
**Upgrade when you need:**
- More than 1 external API integration
- Proper authentication with roles
- Caching for performance
- Production-grade security
- More than 5 entities

**Example:**
```
Started: Simple blog (TIER 1)
Added: User comments, email notifications, image uploads to S3
→ Upgrade to TIER 2
```

### TIER 2 → TIER 3
**Upgrade when you need:**
- Complex integrations (ERP, fiscal systems)
- Message queue for event processing
- Regulatory compliance
- Multi-region deployment
- High availability (99.9%+)
- More than 10 entities

**Example:**
```
Started: E-commerce site (TIER 2)
Added: Integration with warehouse system, accounting software,
       fiscal compliance, multi-country support
→ Upgrade to TIER 3
```

---

## Still Not Sure? Ask Yourself:

### "Can I describe my app in one sentence?"
- **Yes** → Probably TIER 1
- **Takes a paragraph** → Probably TIER 2
- **Needs a full document** → Probably TIER 3

### "How many systems do I integrate with?"
- **0-1** → TIER 1
- **2-4** → TIER 2
- **5+** → TIER 3

### "What happens if it goes down for 1 hour?"
- **Not much** → TIER 1
- **Users are annoyed** → TIER 2
- **Business stops, money lost** → TIER 3

### "Do I have compliance requirements?"
- **No** → TIER 1 or TIER 2
- **Yes** (GDPR, HIPAA, fiscal) → TIER 3

---

## The `/data-app-init` Command Does This For You!

**Good news:** You don't have to score manually!

When you run `/data-app-init`, it will:
1. Ask you 5 targeted questions
2. Calculate the tier automatically
3. Load the appropriate context
4. Show you the estimated time and features

**Example:**
```
You: "Build a data application"

/data-app-init asks:
1. How many entities? → "About 3"
2. External integrations? → "Just email"
3. Scale? → "Small team, maybe 50 users"
4. Special requirements? → "None"
5. Tech preference? → "Node.js"

Result: ✅ Tier 1 detected!
Time: 30-45 minutes
No agents needed
```

---

## Summary Table

| Criteria | TIER 1 | TIER 2 | TIER 3 |
|----------|---------|---------|---------|
| **Entities** | 1-5 | 5-10 | 10+ |
| **Integrations** | 0-1 | 2-4 | 5+ |
| **Users** | <100 | 100-10K | 10K+ |
| **Time** | 30-45 min | 60-90 min | 90-120 min |
| **Agents** | 0 | 1 | 5-6 |
| **Auth** | Basic/Optional | JWT + RBAC | Multi-factor, SSO |
| **Caching** | None | Redis | Multi-layer |
| **Monitoring** | Basic logs | Metrics | Full observability |
| **Deployment** | Simple cloud | Docker + Cloud | Kubernetes |
| **Compliance** | None | Basic | Full (GDPR, etc.) |
| **HA** | No | No | Yes (99.9%+) |
| **Testing** | Basic | Comprehensive | Extensive |

---

## Bottom Line

**When in doubt:**
- Start with **TIER 1** for MVPs and prototypes
- Use **TIER 2** for real business applications
- Use **TIER 3** only for enterprise requirements

**Remember:** It's easier to upgrade from TIER 1 → TIER 2 → TIER 3 than to start with TIER 3 and maintain unnecessary complexity!

The `/data-app-init` command will guide you through the decision automatically. Trust its recommendation! 🎯
