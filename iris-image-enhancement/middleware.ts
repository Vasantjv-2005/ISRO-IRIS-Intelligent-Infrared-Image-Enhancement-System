import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname
  const token = request.cookies.get('auth_token')?.value || request.cookies.get('token')?.value

  // Public routes that don't require authentication
  const publicRoutes = ['/login', '/signup']

  // Protected routes that require authentication
  const protectedRoutes = ['/', '/dashboard']

  // If user is authenticated and tries to access auth pages, redirect to dashboard
  if (token && publicRoutes.includes(pathname)) {
    return NextResponse.redirect(new URL('/', request.url))
  }

  // If user is not authenticated and tries to access protected routes, redirect to login
  if (!token && protectedRoutes.includes(pathname)) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/', '/login', '/signup', '/dashboard'],
}
