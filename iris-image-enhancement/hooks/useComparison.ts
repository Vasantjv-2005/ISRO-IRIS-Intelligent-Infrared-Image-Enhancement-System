'use client'

import { useMutation } from '@tanstack/react-query'
import { toast } from 'sonner'
import { comparisonService } from '@/services/comparison'
import { ComparisonRequestSchema, ComparisonResponseSchema } from '@/types/api'

export function useComparison() {
  const compareMutation = useMutation({
    mutationFn: (data: ComparisonRequestSchema) => comparisonService.compare(data),
    onSuccess: (data: ComparisonResponseSchema) => {
      toast.success(`Comparison analysis completed (Similarity: ${data.similarity_score.toFixed(2)})`)
    },
    onError: (error: any) => {
      const msg = error.response?.data?.detail || error.message || 'Comparison failed'
      toast.error(`Comparison Failed: ${msg}`)
    },
  })

  return {
    compare: compareMutation.mutate,
    compareAsync: compareMutation.mutateAsync,
    isComparing: compareMutation.isPending,
    result: compareMutation.data,
  }
}
