'use client'

import React, { createContext, useContext, useState } from 'react'

export type PipelineStep = 'upload' | 'preprocessing' | 'enhancement' | 'colorization' | 'detection' | 'analysis' | 'export'

interface PipelineState {
  currentStep: PipelineStep
  completedSteps: PipelineStep[]
  isProcessing: boolean
  processingStatus: string
  error: string | null
}

interface PipelineSettings {
  denoise: boolean
  contrastEnhancement: boolean
  enhancementLevel: number
  colormap: string
  superResolution: boolean
  backend: string
  detectionConfidence: number
  geminiContext: string
}

interface PipelineContextType {
  state: PipelineState
  settings: PipelineSettings
  updateStep: (step: PipelineStep) => void
  markStepComplete: (step: PipelineStep) => void
  setIsProcessing: (isProcessing: boolean) => void
  setProcessingStatus: (status: string) => void
  setError: (error: string | null) => void
  updateSettings: (settings: Partial<PipelineSettings>) => void
  resetPipeline: () => void
}

const defaultState: PipelineState = {
  currentStep: 'upload',
  completedSteps: [],
  isProcessing: false,
  processingStatus: '',
  error: null,
}

const defaultSettings: PipelineSettings = {
  denoise: true,
  contrastEnhancement: true,
  enhancementLevel: 2,
  colormap: 'inferno',
  superResolution: true,
  backend: 'huggingface',
  detectionConfidence: 0.5,
  geminiContext: '',
}

const PipelineContext = createContext<PipelineContextType | undefined>(undefined)

export function PipelineProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<PipelineState>(defaultState)
  const [settings, setSettings] = useState<PipelineSettings>(defaultSettings)

  const updateStep = (step: PipelineStep) => {
    setState((prev) => ({ ...prev, currentStep: step }))
  }

  const markStepComplete = (step: PipelineStep) => {
    setState((prev) => ({
      ...prev,
      completedSteps: prev.completedSteps.includes(step) ? prev.completedSteps : [...prev.completedSteps, step],
    }))
  }

  const setIsProcessing = (isProcessing: boolean) => {
    setState((prev) => ({ ...prev, isProcessing }))
  }

  const setProcessingStatus = (status: string) => {
    setState((prev) => ({ ...prev, processingStatus: status }))
  }

  const setError = (error: string | null) => {
    setState((prev) => ({ ...prev, error }))
  }

  const updateSettings = (newSettings: Partial<PipelineSettings>) => {
    setSettings((prev) => ({ ...prev, ...newSettings }))
  }

  const resetPipeline = () => {
    setState(defaultState)
    setSettings(defaultSettings)
  }

  return (
    <PipelineContext.Provider
      value={{
        state,
        settings,
        updateStep,
        markStepComplete,
        setIsProcessing,
        setProcessingStatus,
        setError,
        updateSettings,
        resetPipeline,
      }}
    >
      {children}
    </PipelineContext.Provider>
  )
}

export function usePipeline() {
  const context = useContext(PipelineContext)
  if (context === undefined) {
    throw new Error('usePipeline must be used within PipelineProvider')
  }
  return context
}
