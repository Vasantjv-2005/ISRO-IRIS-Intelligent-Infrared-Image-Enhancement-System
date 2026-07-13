'use client'

import { useQuery } from '@tanstack/react-query'
import { dashboardService } from '@/services/dashboard'
import { DashboardResponseSchema } from '@/types/api'

export function useDashboard() {
  const query = useQuery<DashboardResponseSchema>({
    queryKey: ['dashboard'],
    queryFn: () => dashboardService.getDashboardData(),
    refetchInterval: 15000, // Refresh every 15s for live telemetry
  })

  return {
    data: query.data,
    isLoading: query.isLoading,
    isError: query.isError,
    error: query.error,
    refetch: query.refetch,
  }
}
