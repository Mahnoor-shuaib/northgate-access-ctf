# Northgate Access: Solution Writeup

**Category:** Web  
**Difficulty:** Easy  
**Vulnerability:** Broken Access Control (client-side role stored in a cookie)  
**Flag:** `CGS{t34ch3r_c00k13_h4ck}`

> Organiser document. Do not share with participants.

---

## Overview

Northgate Student Portal is a small Flask site with no login. The server decides what a visitor may see
by reading a `role` cookie. Visitors get `role=student` automatically, and the faculty gradebook
(`/faculty`) is only supposed to open for `role=teacher`. The cookie lives in the browser, so the visitor can change it.

---

## Solution

### Step 1: Open the portal

Visit the site. The header and the ID card show the current role: `student`.

### Step 2: Try the faculty gradebook

Click **Faculty Gradebook** (or open `/faculty`). The page says access is denied and that the gradebook
is for users with the **teacher** role. It also shows the current role.

### Step 3: Look at the cookie

Open browser DevTools (`F12`):

- Chrome / Edge: **Application > Cookies > the site**
- Firefox: **Storage > Cookies**

There is one cookie:

| Name | Value |
|---|---|
| `role` | `student` |

### Step 4: Change the cookie

Change the value from `student` to `teacher`.

### Step 5: Reload `/faculty`

The server trusts the cookie, so the gradebook opens. The **Exam vault** card shows the master key:

```
CGS{t34ch3r_c00k13_h4ck}
```

---

## Solve flow at a glance

```
Open site -> Click Faculty Gradebook -> Access denied (needs "teacher")
-> DevTools -> role=student -> change to role=teacher -> reload /faculty -> Flag
```

---

## Root cause (the vulnerable code)

```python
def current_role():
    return request.cookies.get("role", "student").strip().lower()

@app.route("/faculty")
def faculty():
    if current_role() != "teacher":
        return page("denied.html", status=403)
    return page("faculty.html", gradebook=GRADEBOOK, flag=FLAG)
```

The server uses a value controlled by the user (the cookie) to make an authorization decision.

## How to fix it

- Store the role on the **server**: log the user in and keep the role in a server-side session or database.
- If a cookie is needed, use a **signed** session (for example Flask's `session`) so the user cannot edit it.
- Never trust data from the client (cookies, headers, hidden form fields) for access decisions.

---

## Notes for organisers

- Keep this file in the project root, **not** inside `static/` or `templates/`, because Flask serves `static/` publicly.
- The default flag can be changed with the `FLAG` environment variable. Keep the full flag (including `CGS{` and `}`) between 19 and 25 characters.
- No data is stored, so there is nothing to reset and multiple workers are fine.
