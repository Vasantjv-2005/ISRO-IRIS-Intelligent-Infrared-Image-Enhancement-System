'use client'

import React, { createContext, useContext, useState } from 'react'

export type CommandView = 'workspace' | 'dashboard' | 'history'

interface ViewContextType {
  activeView: CommandView
  setActiveView: (view: CommandView) => void
}

const ViewContext = createContext<ViewContextType | undefined>(undefined)

export function ViewProvider({ children }: { children: React.ReactNode }) {
  const [activeView, setActiveView] = useState<CommandView>('workspace')

  return (
    <ViewContext.Provider value={{ activeView, setActiveView }}>
      {children}
    </ViewContext.Provider>
  )
}

export function useView() {
  const context = useContext(ViewContext)
  if (!context) {
    throw new Error('useView must be used within ViewProvider')
  }
  return context
}
