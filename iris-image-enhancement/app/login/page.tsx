'use client'

import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { Eye, EyeOff, AlertCircle, Loader2 } from 'lucide-react'
import { login } from '@/lib/api'
import { GlassCard } from '@/components/ui/GlassCard'

export default function LoginPage() {
  const router = useRouter()
  const [mounted, setMounted] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    setMounted(true)
  }, [])

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await login(email, password)
      const payload = response?.data || response
      const token = payload?.access_token
      const userData = payload?.user || { email }

      if (token) {
        localStorage.setItem('token', token)
        localStorage.setItem('auth_token', token)
        localStorage.setItem('user', JSON.stringify(userData))
        localStorage.setItem('auth_user', JSON.stringify(userData))
        document.cookie = `auth_token=${token}; path=/; max-age=86400; SameSite=Lax`
        document.cookie = `token=${token}; path=/; max-age=86400; SameSite=Lax`
        window.location.href = '/'
      } else {
        setError('Authentication succeeded but token was missing. Please try again.')
      }
    } catch (err: any) {
      const detail = err.response?.data?.detail
      const errMsg =
        typeof detail === 'string'
          ? detail
          : Array.isArray(detail)
            ? detail.map((d: any) => d.msg).join(', ')
            : err.message || 'Login failed. Please try again.'
      setError(errMsg)
    } finally {
      setLoading(false)
    }
  }

  if (!mounted) return null

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4 py-12">
      {/* Animated background glow */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
          <div className="w-96 h-96 bg-primary/10 rounded-full blur-3xl opacity-30 animate-pulse" />
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-md relative z-10"
      >
        {/* Logo & Branding */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.4 }}
          className="text-center mb-8"
        >
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-xl bg-gradient-to-br from-primary/20 to-secondary/20 border border-primary/30 mb-4">
            <span className="text-2xl">🛰️</span>
          </div>
          <h1 className="text-3xl font-bold text-foreground mb-1">ISRO IRIS</h1>
          <p className="text-sm text-muted-foreground">Thermal Imaging Command Center</p>
        </motion.div>

        {/* Login Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.4 }}
        >
          <GlassCard>
            <div className="p-8">
              <h2 className="text-xl font-bold text-foreground mb-6">Mission Access</h2>

              <form onSubmit={handleLogin} className="space-y-4">
                {/* Error Alert */}
                {error && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-start gap-3 p-3 rounded-lg bg-destructive/10 border border-destructive/30"
                  >
                    <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-destructive">{error}</p>
                  </motion.div>
                )}

                {/* Email Field */}
                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="commander@isro.gov.in"
                    className="w-full px-4 py-2.5 rounded-lg bg-input border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
                    required
                    disabled={loading}
                  />
                </div>

                {/* Password Field */}
                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    Password
                  </label>
                  <div className="relative">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      className="w-full px-4 py-2.5 rounded-lg bg-input border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
                      required
                      disabled={loading}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                      disabled={loading}
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-2.5 rounded-lg font-semibold text-sm transition-all duration-300 flex items-center justify-center gap-2
                    bg-primary text-primary-foreground hover:shadow-[0_0_20px_rgba(0,240,255,0.5)]
                    active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Authenticating...
                    </>
                  ) : (
                    <>
                      <span>🔓</span>
                      Access Command Center
                    </>
                  )}
                </button>
              </form>

              {/* Divider */}
              <div className="relative my-6">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full h-px bg-gradient-to-r from-border via-primary/20 to-border" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-card text-muted-foreground">New to IRIS?</span>
                </div>
              </div>

              {/* Sign Up Link */}
              <Link href="/signup">
                <motion.button
                  type="button"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full py-2.5 rounded-lg font-semibold text-sm transition-all duration-300
                    border border-secondary/50 text-secondary hover:border-secondary hover:bg-secondary/10"
                >
                  Create Account
                </motion.button>
              </Link>
            </div>
          </GlassCard>
        </motion.div>

        {/* Footer Info */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.4 }}
          className="mt-6 text-center text-xs text-muted-foreground"
        >
          <p>🔒 Secure thermal imaging authentication system</p>
          <p className="mt-1">Powered by ISRO Deep Space Technologies</p>
        </motion.div>
      </motion.div>
    </div>
  )
}
