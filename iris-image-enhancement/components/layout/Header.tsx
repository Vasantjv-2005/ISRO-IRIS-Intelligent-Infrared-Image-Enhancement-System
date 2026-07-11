'use client'

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Satellite, Signal, LogOut, LogIn, UserPlus } from 'lucide-react'
import Link from 'next/link'
import { useAuth } from '@/lib/context/AuthContext'
import { systemAPI } from '@/lib/api'
import { Badge } from '@/components/ui/Badge'

export function Header() {
  const { user, logout } = useAuth()
  const [isHealthy, setIsHealthy] = useState(false)
  const [latency, setLatency] = useState(0)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const start = Date.now()
        await systemAPI.health()
        setLatency(Date.now() - start)
        setIsHealthy(true)
      } catch {
        setIsHealthy(false)
      }
    }

    checkHealth()
    const interval = setInterval(checkHealth, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-primary/20 bg-background/85 backdrop-blur-2xl shadow-[0_4px_30px_rgba(0,0,0,0.5)]">
      <div className="flex items-center justify-between px-6 py-3">
        {/* Left: Branding & Orbital Radar Emblem */}
        <motion.div className="flex items-center gap-3.5" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
          <div className="relative flex items-center justify-center w-11 h-11 rounded-xl bg-gradient-to-br from-primary/30 via-primary/10 to-secondary/20 border border-primary/40 shadow-[0_0_20px_rgba(0,240,255,0.25)]">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 12, repeat: Infinity, ease: 'linear' }}
              className="absolute inset-0.5 rounded-xl border border-dashed border-primary/40"
            />
            <Satellite className="w-6 h-6 text-primary drop-shadow-[0_0_8px_rgba(0,240,255,0.8)]" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-extrabold tracking-tight bg-gradient-to-r from-primary via-teal-300 to-white bg-clip-text text-transparent">
                ISRO IRIS
              </h1>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider bg-primary/15 text-primary border border-primary/30">
                CHANDRA-09
              </span>
            </div>
            <p className="text-[11px] font-medium text-muted-foreground tracking-wide">
              INTELLIGENT INFRARED INTERPRETATION SYSTEM
            </p>
          </div>
        </motion.div>

        {/* Center: Aerospace Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-1.5 p-1 rounded-xl bg-card/60 border border-border/60 backdrop-blur-md">
          {[
            { label: 'Tactical Command', href: '#dashboard', active: true },
            { label: 'Neural Workspace', href: '#workspace', active: false },
            { label: 'Mission Dossiers', href: '#history', active: false },
          ].map((item) => (
            <a
              key={item.label}
              href={item.href}
              className={`relative px-4 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all ${
                item.active
                  ? 'bg-primary/20 text-primary border border-primary/40 shadow-[0_0_15px_rgba(0,240,255,0.2)]'
                  : 'text-muted-foreground hover:text-foreground hover:bg-primary/5'
              }`}
            >
              {item.label}
            </a>
          ))}
        </nav>

        {/* Right: Status & User */}
        <div className="flex items-center gap-3">
          {/* System Status */}
          <motion.div className="flex items-center gap-2" whileHover={{ scale: 1.04 }}>
            <div
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-mono font-semibold shadow-sm ${
                isHealthy
                  ? 'bg-green-500/10 text-green-400 border border-green-500/30'
                  : 'bg-red-500/10 text-red-400 border border-red-500/30'
              }`}
            >
              <motion.div
                className={`w-2 h-2 rounded-full ${isHealthy ? 'bg-green-400' : 'bg-red-400'} status-pulse`}
                animate={{ scale: [1, 1.3, 1] }}
                transition={{ duration: 1.8, repeat: Infinity }}
              />
              <Signal className="w-3.5 h-3.5" />
              <span>{latency > 0 ? `${latency}ms` : 'LIVE'}</span>
            </div>
          </motion.div>

          {/* User Info or Auth Links */}
          {user ? (
            <div className="hidden sm:flex items-center gap-3 pl-2 border-l border-border">
              <div className="text-right">
                <p className="text-sm font-bold text-foreground">{user.full_name}</p>
                <p className="text-[10px] text-muted-foreground">{user.email}</p>
              </div>
              <motion.button
                onClick={logout}
                whileHover={{ scale: 1.08 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 rounded-lg bg-destructive/15 hover:bg-destructive/25 text-destructive border border-destructive/30 transition-all"
                title="Logout"
              >
                <LogOut className="w-4 h-4" />
              </motion.button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link href="/login">
                <motion.button
                  whileHover={{ scale: 1.04 }}
                  whileTap={{ scale: 0.95 }}
                  className="hidden sm:flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold text-foreground border border-primary/40 hover:border-primary hover:bg-primary/15 transition-all"
                >
                  <LogIn className="w-3.5 h-3.5" />
                  Login
                </motion.button>
              </Link>
              <Link href="/signup">
                <motion.button
                  whileHover={{ scale: 1.04 }}
                  whileTap={{ scale: 0.95 }}
                  className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold bg-gradient-to-r from-primary to-secondary text-primary-foreground shadow-[0_0_15px_rgba(0,240,255,0.4)] transition-all"
                >
                  <UserPlus className="w-3.5 h-3.5" />
                  Join IRIS
                </motion.button>
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
