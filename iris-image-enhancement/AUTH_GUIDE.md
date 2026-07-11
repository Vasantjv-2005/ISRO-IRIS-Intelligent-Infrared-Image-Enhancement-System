# IRIS Authentication System Guide

## Overview

The IRIS Thermal Imaging Command Center now includes a complete, production-ready authentication system with beautiful, aerospace-themed login and signup pages.

## Features

### Authentication Pages

#### Login Page (`/login`)
- **Beautiful glassmorphic dark design** with electric cyan accents
- Email and password authentication fields
- Show/hide password toggle with eye icon
- Error handling with alert messages
- "Forgot Password?" link ready for implementation
- "Join IRIS" link to signup page
- Responsive design for all screen sizes
- Smooth Framer Motion animations
- System status indicator (ping latency, connection health)

**Route**: `/app/login/page.tsx`

#### Signup Page (`/signup`)
- Full name, email, password, and confirm password fields
- **Real-time password strength meter** with visual feedback
- Password validation rules:
  - Minimum 8 characters
  - Must include uppercase letter
  - Must include numbers
  - Special characters for bonus strength
- Automatic password match validation
- Animated strength indicators (weak, fair, strong)
- Error and success alerts
- Auto-redirect to dashboard after successful signup
- Link back to login page
- Enterprise-grade security messaging

**Route**: `/app/signup/page.tsx`

### State Management

#### AuthContext (`/lib/context/AuthContext.tsx`)
Manages global authentication state:
- `user` - Current logged-in user object
- `token` - JWT access token
- `isLoading` - Loading state during auth operations
- `error` - Error messages for display
- `login()` - Login with email/password
- `register()` - Create new account
- `logout()` - Clear session and localStorage

**Usage**:
```typescript
import { useAuth } from '@/lib/context/AuthContext'

function MyComponent() {
  const { user, login, logout } = useAuth()
  // Use auth state and methods
}
```

### API Integration

#### Auth Endpoints (`/lib/api.ts`)
All endpoints are pre-configured:

```typescript
// Login
POST /auth/login
Body: { email: string, password: string }
Response: { access_token: string, user: User }

// Register
POST /auth/register
Body: { full_name: string, email: string, password: string, confirm_password: string }
Response: { access_token: string, user: User }
```

**Helper Functions**:
```typescript
import { login, register } from '@/lib/api'

// Usage in pages
await login(email, password)
await register(fullName, email, password, confirmPassword)
```

### Session Management

#### Token Storage
- Stored in `localStorage` as `auth_token`
- User info stored in `localStorage` as `auth_user`
- Automatically restored on app reload
- Cleared on logout

#### Token Injection
All API requests automatically include JWT token:
```
Authorization: Bearer <token>
```

This is handled by the Axios interceptor in `lib/api.ts`.

### Route Protection

#### Middleware (`/middleware.ts`)
- Redirects unauthenticated users to `/login`
- Redirects authenticated users away from auth pages
- Protected routes: `/`, `/dashboard`
- Public routes: `/login`, `/signup`

**Behavior**:
- No token + accessing `/` → Redirect to `/login`
- No token + accessing `/login` → Stay on login page
- With token + accessing `/` → Access dashboard
- With token + accessing `/login` → Redirect to `/`

### UI Components

#### Header Authentication Display
The Header component (`/components/layout/Header.tsx`) now shows:

**When authenticated**:
- User's full name
- User's email
- Logout button
- System status indicator

**When not authenticated**:
- Login link
- "Join IRIS" button
- System status indicator

## Styling & Design

### Color System
- **Background**: Deep obsidian (#0B0E14)
- **Primary Accent**: Electric cyan (#00F0FF) - buttons, focus states
- **Secondary Accent**: Quantum teal (#00D2B4) - success, secondary actions
- **Accent**: Plasma magenta (#E01E79) - alerts, highlights
- **Input Background**: Semi-transparent dark (rgb(15 20 32 / 0.8))
- **Borders**: Subtle cyan glow (rgba(0 240 255 / 0.15))

### Typography
- **Headings**: Inter, bold, modern geometry
- **Labels**: Inter, medium weight
- **Input text**: Inter, regular weight
- **Monospace**: JetBrains Mono (for code-like displays)

### Animations
- Page fade-in on mount
- Smooth field transitions
- Button hover glow effect (0_0_20px_rgba(0,240,255,0.5))
- Password strength bar animation
- Error/success alert slides
- Form transitions on submit

## Security Features

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one number
- Optional special characters for extra strength

### Form Validation
- Email format validation
- Password strength checking
- Confirm password matching
- Field-level error messages
- Real-time feedback

### Token Security
- JWT authentication
- Token stored in localStorage (accessible only to JS, not cookies - evaluate for security needs)
- Token automatically injected to API requests
- Unauthorized (401) responses clear token
- Password never stored in localStorage

### Error Handling
- User-friendly error messages
- Error alerts with icons
- Prevents double-submit on errors
- Validates before sending to API

## Testing the Auth Flow

### Test Login
1. Open http://localhost:3000
2. Get redirected to /login (no token)
3. Enter test credentials
4. Click "Access Command Center"
5. Token saved, redirected to dashboard

### Test Signup
1. Go to http://localhost:3000/signup
2. Fill in form:
   - Full Name: Dr. Test User
   - Email: test@example.com
   - Password: TestPassword123 (meets requirements)
   - Confirm: TestPassword123
3. Watch password strength meter
4. Click "Create Account"
5. Success message and redirect to dashboard

### Test Logout
1. On dashboard, click logout button (top right)
2. Token cleared from localStorage
3. Next access to / redirects to login

### Test Protected Routes
- Accessing / without token → redirected to /login
- Accessing /login with token → redirected to /
- System properly enforces authentication

## Customization

### Changing Colors
Edit `/app/globals.css`:
```css
:root {
  --primary: #00f0ff;  /* Change this */
  --secondary: #00d2b4;
  --accent: #e01e79;
  /* ... */
}
```

### Modifying Form Fields
- Edit `/app/login/page.tsx` or `/app/signup/page.tsx`
- Add new fields as needed
- Update API call to match backend

### Adjusting Animations
- Edit `initial`, `animate`, `transition` props in Framer Motion components
- Find `motion.` components in auth pages
- Modify timing and effects

### Changing Validation Rules
Edit password validation in `/app/signup/page.tsx`:
```typescript
const validatePassword = (pwd: string) => {
  // Modify requirements here
  return pwd.length >= 8 && /[A-Z]/.test(pwd) && /[0-9]/.test(pwd)
}
```

## Integration with Backend

### Backend Requirements
Your backend must provide:
- `POST /auth/login` endpoint
- `POST /auth/register` endpoint
- Return `access_token` and `user` object
- Support Bearer token authentication
- Handle JWT validation

### Backend Response Format
```json
{
  "access_token": "eyJhbGc...",
  "user": {
    "id": "user-123",
    "email": "commander@isro.gov.in",
    "full_name": "Dr. Commander"
  }
}
```

## Common Tasks

### Add Remember Me
Edit login page checkbox:
```typescript
<input
  type="checkbox"
  checked={rememberMe}
  onChange={(e) => setRememberMe(e.target.checked)}
/>
```

### Add Social Login
```typescript
<button onClick={loginWithGoogle}>
  Login with Google
</button>
```

### Change Redirect After Login
In `/app/login/page.tsx`:
```typescript
if (response.access_token) {
  router.push('/dashboard')  // Change this path
}
```

### Add Email Verification
- Backend validates email
- Frontend shows "Verify your email" message
- User confirms email link
- Account activated

### Add Password Reset
Create `/app/forgot-password/page.tsx`:
```typescript
const handleReset = async (email: string) => {
  await api.post('/auth/forgot-password', { email })
  // Show "Check your email" message
}
```

## Known Limitations & TODOs

- [ ] Implement "Forgot Password" flow
- [ ] Add email verification on signup
- [ ] Add social login (Google, GitHub)
- [ ] Add 2FA support
- [ ] Move token to secure HTTP-only cookie
- [ ] Implement refresh token rotation
- [ ] Add rate limiting on login attempts
- [ ] Add audit logging for auth events

## File Structure

```
/app
├── login/
│   └── page.tsx         # Beautiful login form
├── signup/
│   └── page.tsx         # Account creation form
├── page.tsx             # Dashboard (protected)
├── layout.tsx           # Root layout
├── globals.css          # Dark theme colors
└── middleware.ts        # Route protection

/lib
├── api.ts               # Auth endpoints & helpers
└── context/
    └── AuthContext.tsx  # Global auth state

/components/
├── layout/
│   └── Header.tsx       # Auth display in header
└── ui/
    ├── GlassCard.tsx    # Reusable auth card
    ├── Badge.tsx        # Status badges
    └── Spinner.tsx      # Loading indicators
```

## Support

For issues or questions:
1. Check browser console for errors
2. Verify backend is running at http://127.0.0.1:8000
3. Check localStorage for auth_token
4. Test API endpoints with Postman/curl

---

**Built with**: Next.js 16 + React 19 + TypeScript + Framer Motion + Tailwind CSS

**Status**: Production-ready authentication system
