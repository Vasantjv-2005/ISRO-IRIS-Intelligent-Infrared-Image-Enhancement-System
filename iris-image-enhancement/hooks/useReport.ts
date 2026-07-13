'use client'

import { useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { reportService } from '@/services/report'
import { downloadService } from '@/services/download'
import { ReportRequestSchema, ReportResponseSchema } from '@/types/api'

export function useReport() {
  const queryClient = useQueryClient()

  const generateMutation = useMutation({
    mutationFn: (data: ReportRequestSchema) => reportService.generate(data),
    onSuccess: (data: ReportResponseSchema) => {
      toast.success('ISRO IRIS PDF Report generated successfully')
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
    },
    onError: (error: any) => {
      const msg = error.response?.data?.detail || error.message || 'Report generation failed'
      toast.error(`Report Generation Failed: ${msg}`)
    },
  })

  const downloadReport = async (reportPath: string, customName?: string) => {
    try {
      toast.info('Downloading PDF Report dossier...')
      await downloadService.triggerDownload(reportPath, customName)
      toast.success('PDF Report downloaded')
    } catch (error: any) {
      toast.error('Failed to download PDF report')
    }
  }

  return {
    generateReport: generateMutation.mutate,
    generateReportAsync: generateMutation.mutateAsync,
    isGenerating: generateMutation.isPending,
    reportData: generateMutation.data,
    downloadReport,
  }
}
