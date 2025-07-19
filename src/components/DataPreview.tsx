import React, { useMemo } from 'react'
import {
  Box,
  Typography,
  Chip,
  useTheme,
} from '@mui/material'
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid'
import { Visibility, TableRows } from '@mui/icons-material'

interface QVDData {
  columns: string[]
  rows: Record<string, any>[]
  totalRows: number
}

interface DataPreviewProps {
  data: QVDData
  selectedColumns: string[]
}

const DataPreview: React.FC<DataPreviewProps> = ({ data, selectedColumns }) => {
  const theme = useTheme()

  const columns: GridColDef[] = useMemo(() => {
    return selectedColumns.map((column) => ({
      field: column,
      headerName: column,
      flex: 1,
      minWidth: 150,
      renderCell: (params: GridRenderCellParams) => {
        const value = params.value
        if (value === '' || value === null || value === undefined) {
          return (
            <Typography
              variant="body2"
              sx={{ color: 'text.disabled', fontStyle: 'italic' }}
            >
              (vacío)
            </Typography>
          )
        }
        return (
          <Typography variant="body2" noWrap title={String(value)}>
            {String(value)}
          </Typography>
        )
      },
      renderHeader: () => (
        <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
          {column}
        </Typography>
      ),
    }))
  }, [selectedColumns])

  const rows = useMemo(() => {
    return data.rows.map((row, index) => ({
      id: index,
      ...row,
    }))
  }, [data.rows])

  const filteredRows = useMemo(() => {
    return rows.map(row => {
      const filteredRow: any = { id: row.id }
      selectedColumns.forEach(col => {
        filteredRow[col] = row[col]
      })
      return filteredRow
    })
  }, [rows, selectedColumns])

  if (selectedColumns.length === 0) {
    return (
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        sx={{
          minHeight: 200,
          backgroundColor: theme.palette.grey[50],
          borderRadius: 2,
          border: `1px dashed ${theme.palette.grey[300]}`,
        }}
      >
        <Visibility sx={{ fontSize: 48, color: 'text.disabled', mb: 2 }} />
        <Typography variant="h6" color="text.secondary" gutterBottom>
          Selecciona columnas para ver la vista previa
        </Typography>
        <Typography variant="body2" color="text.disabled">
          Marca las columnas que deseas incluir en la exportación
        </Typography>
      </Box>
    )
  }

  return (
    <Box>
      <Box display="flex" alignItems="center" gap={2} mb={2}>
        <Box display="flex" alignItems="center" gap={1}>
          <TableRows color="primary" />
          <Typography variant="subtitle2">
            Mostrando {Math.min(data.rows.length, 100)} de {data.totalRows} filas
          </Typography>
        </Box>
        <Chip
          label={`${selectedColumns.length} columnas`}
          size="small"
          color="primary"
          variant="outlined"
        />
      </Box>

      <Box sx={{ height: 400, width: '100%' }}>
        <DataGrid
          rows={filteredRows}
          columns={columns}
          initialState={{
            pagination: {
              paginationModel: {
                pageSize: 10,
              },
            },
          }}
          pageSizeOptions={[5, 10, 25]}
          disableRowSelectionOnClick
          sx={{
            '& .MuiDataGrid-header': {
              backgroundColor: theme.palette.primary.main,
              color: 'white',
            },
            '& .MuiDataGrid-columnHeader': {
              backgroundColor: theme.palette.primary.main,
              color: 'white',
            },
            '& .MuiDataGrid-columnHeaderTitle': {
              color: 'white',
              fontWeight: 'bold',
            },
            '& .MuiDataGrid-menuIconButton': {
              color: 'white',
            },
            '& .MuiDataGrid-sortIcon': {
              color: 'white',
            },
            '& .MuiDataGrid-row:hover': {
              backgroundColor: theme.palette.action.hover,
            },
            '& .MuiDataGrid-cell': {
              borderBottom: `1px solid ${theme.palette.divider}`,
            },
            border: `1px solid ${theme.palette.divider}`,
            borderRadius: 2,
          }}
        />
      </Box>

      <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
        Nota: La vista previa muestra un máximo de 100 filas. La exportación incluirá todas las {data.totalRows} filas.
      </Typography>
    </Box>
  )
}

export default DataPreview