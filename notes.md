Bilkul bro ❤️ Abhi tak humne **GraphQL ke kaafi important concepts** touch kiye hain. Main tumhein ek simple **memory map** deta hoon taa ke concepts dimagh mein connected rahen.

## 🧠 GraphQL ka simple flow

Socho tumhara backend ek **restaurant** hai:

```text
Client
  ↓
GraphQL
  ↓
Query / Mutation
  ↓
Resolver
  ↓
Database
  ↓
Response
```

Ab ek ek concept:

### 1. Schema 📋

**Schema = API ka blueprint / contract**

Ye batata hai:

> API mein kaunsa data available hai aur kya operations ki ja sakti hain.

Example:

```graphql
type Product {
    id: Int!
    name: String!
    price: Float!
}
```

**Yaad rakho:**
👉 Schema = **API ka naqsha**

---

### 2. Type 🧱

**Type = data ka structure**

Humne:

```python
@strawberry.type
class Product:
    id: int
    name: str
    description: str
    price: float
    quantity: int
```

banaya.

Matlab Product ke andar ye fields hain.

**Yaad rakho:**
👉 Type = **data kaisa dikhega**

---

### 3. Field 🔹

Product ke andar:

```text
id
name
description
price
quantity
```

har ek **field** hai.

**Yaad rakho:**
👉 Field = **data ka ek particular piece**

---

### 4. Query 🔍

**Query = data read karna**

Humne:

```graphql
query {
    products {
        id
        name
        price
    }
}
```

Aur:

```graphql
query {
    product(id: 1) {
        id
        name
        price
    }
}
```

banaya.

**Yaad rakho:**

> Query = **GET / read**

REST se compare karo:

```text
REST GET       → GraphQL Query
```

---

### 5. Resolver ⚙️

Ye **bohat important concept** hai.

Resolver wo Python function hai jo actually decide karta hai:

> "Client ne ye data manga hai, main usko data kahan se laa kar doon?"

Example:

```python
@strawberry.field
def products(self) -> list["Product"]:
    return [
        Product(...),
        Product(...)
    ]
```

Ye function **resolver** hai.

GraphQL request:

```graphql
query {
    products {
        name
    }
}
```

↓

GraphQL resolver ko call karta hai

↓

```python
products()
```

↓

data return hota hai.

**Yaad rakho:**

> Resolver = **GraphQL request ka actual kaam karne wala function**

Simple:

```text
Query = "Mujhe products chahiye"
Resolver = "Ye lo products"
```

---

### 6. Input Type 📥

Abhi humne:

```python
@strawberry.input
class ProductInput:
    name: str
    description: str
    price: float
    quantity: int
```

banaya.

Ye **client se data receive** karne ke liye hai.

Example:

```graphql
mutation {
    createProduct(
        product: {
            name: "Keyboard"
            price: 75.5
            quantity: 10
        }
    )
}
```

Yahan jo data aa raha hai wo `ProductInput` mein jayega.

**Yaad rakho:**

```text
@strawberry.type
→ Response

@strawberry.input
→ Request/Input
```

Ye difference yaad rakhna bohat important hai. 🔥

---

### 7. Mutation ✏️

**Mutation = data change karna**

Jaise:

```text
Create
Update
Delete
```

Humne:

```python
@strawberry.mutation
def create_product(...)
```

banaya.

REST mein:

```text
POST    → Create
PUT/PATCH → Update
DELETE  → Delete
```

GraphQL mein generally:

```text
Mutation → Create / Update / Delete
```

**Yaad rakho:**

> Mutation = **database/data mein change**

---

## 🧠 Ab sab ko ek diagram mein yaad karo

```text
                 GRAPHQL
                    │
          ┌─────────┴─────────┐
          │                   │
        Query              Mutation
          │                   │
       Read Data          Change Data
          │                   │
          └─────────┬─────────┘
                    ↓
                 Resolver
                    ↓
               Data Source
             (abhi dummy data)
                    ↓
                Response
```

Aur:

```text
Type
 ↓
Response ka structure

Input
 ↓
Client se aane wale data ka structure
```

---

## 🔥 One-line cheat sheet

Isko yaad kar lo:

| Concept      | Simple meaning                  |
| ------------ | ------------------------------- |
| **Schema**   | API ka blueprint                |
| **Type**     | Data ka structure               |
| **Field**    | Data ka ek part                 |
| **Query**    | Data read karna                 |
| **Resolver** | Request ka actual kaam karna    |
| **Input**    | Client se data lena             |
| **Mutation** | Data create/update/delete karna |

### Sabse important 3:

```text
Query    = Mujhe data do 🔍
Mutation = Data change karo ✏️
Resolver = Ye kaam main karta hoon ⚙️
```

Aur bro, **Subscriptions** abhi humne nahi kiye. Wo baad mein aayenge:

```text
Subscription = "Data change ho to mujhe automatically update karna." 🔴
```

Abhi tumhare GraphQL fundamentals ka base **Schema → Type → Query → Resolver → Input → Mutation** tak ban chuka hai. 💪
