'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { authAPI } from '@/lib/api'

interface User {
  id: string
  email: string
  full_name: string
}

interface AuthContextType {
  user: User | null
  token: string | null
  isLoading: boolean
  error: string | null
  login: (email: string, password: string) => Promise<void>
  register: (full_name: string, email: string, password: string, confirm_password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Restore session from localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token') || localStorage.getItem('token')
    const storedUser = localStorage.getItem('auth_user') || localStorage.getItem('user')
    if (storedToken && storedUser) {
      setToken(storedToken)
      document.cookie = `auth_token=${storedToken}; path=/; max-age=86400; SameSite=Lax`
      document.cookie = `token=${storedToken}; path=/; max-age=86400; SameSite=Lax`
      try {
        setUser(JSON.parse(storedUser))
      } catch {
        setUser({ email: 'User' } as any)
      }
    }
    setIsLoading(false)
  }, [])

  const login = async (email: string, password: string) => {
    setIsLoading(true)
    setError(null)
    try {
      const response = await authAPI.login({ email, password })
      const payload = response?.data || response
      const access_token = payload?.access_token
      const userData = payload?.user || { email }
      setToken(access_token)
      setUser(userData)
      localStorage.setItem('auth_token', access_token)
      localStorage.setItem('token', access_token)
      localStorage.setItem('auth_user', JSON.stringify(userData))
      localStorage.setItem('user', JSON.stringify(userData))
      document.cookie = `auth_token=${access_token}; path=/; max-age=86400; SameSite=Lax`
      document.cookie = `token=${access_token}; path=/; max-age=86400; SameSite=Lax`
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Login failed'
      setError(message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (full_name: string, email: string, password: string, confirm_password: string) => {
    setIsLoading(true)
    setError(null)
    try {
      const response = await authAPI.register({ full_name, email, password, confirm_password })
      const payload = response?.data || response
      const access_token = payload?.access_token
      const userData = payload?.user || { email, full_name }
      setToken(access_token)
      setUser(userData)
      localStorage.setItem('auth_token', access_token)
      localStorage.setItem('token', access_token)
      localStorage.setItem('auth_user', JSON.stringify(userData))
      localStorage.setItem('user', JSON.stringify(userData))
      document.cookie = `auth_token=${access_token}; path=/; max-age=86400; SameSite=Lax`
      document.cookie = `token=${access_token}; path=/; max-age=86400; SameSite=Lax`
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Registration failed'
      setError(message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('auth_token')
    localStorage.removeItem('token')
    localStorage.removeItem('auth_user')
    localStorage.removeItem('user')
    document.cookie = 'auth_token=; path=/; max-age=0'
    document.cookie = 'token=; path=/; max-age=0'
  }

  return (
    <AuthContext.Provider value={{ user, token, isLoading, error, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
