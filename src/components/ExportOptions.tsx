import React, { useState } from 'react'
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  TextField,
  Typography,
  Divider,
  Alert,
} from '@mui/material'
import { Download, Settings } from '@mui/icons-material'

interface QVDData {
  columns: string[]
  rows: Record<string, any>[]
  totalRows: number
}

interface ExportOptionsProps {
  data: QVDData
  selectedColumns: string[]
}

const ExportOptions: React.FC<ExportOptionsProps> = ({ data, selectedColumns }) => {
  const [delimiter, setDelimiter] = useState(',')
  const [encoding, setEncoding] = useState('utf-8')
  const [includeHeaders, setIncludeHeaders] = useState(true)
  const [fileName, setFileName] = useState('exported_data')

  const generateCSV = () => {
    if (selectedColumns.length === 0) {
      return
    }

    const headers = selectedColumns
    const rows = data.rows.map(row => 
      selectedColumns.map(col => {
        const value = row[col]
        // Escapar comillas y manejar valores que contengan el delimitador
        if (typeof value === 'string' && (value.includes(delimiter) || value.includes('"') || value.includes('\n'))) {
          return `"${value.replace(/"/g, '""')}"`
        }
        return value || ''
      })
    )

    let csvContent = ''
    
    if (includeHeaders) {
      csvContent += headers.join(delimiter) + '\n'
    }
    
    csvContent += rows.map(row => row.join(delimiter)).join('\n')

    return csvContent
  }

  const handleDownload = () => {
    const csvContent = generateCSV()
    if (!csvContent) return

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', `${fileName}.csv`)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  const previewData = () => {
    const filteredRows = data.rows.slice(0, 3).map(row => 
      selectedColumns.reduce((filtered, col) => {
        filtered[col] = row[col]
        return filtered
      }, {} as Record<string, any>)
    )
    return filteredRows
  }

  return (
    <Box>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <Settings />
        <Typography variant="subtitle2">Configuración</Typography>
      </Box>

      <TextField
        fullWidth
        label="Nombre del archivo"
        value={fileName}
        onChange={(e) => setFileName(e.target.value)}
        size="small"
        sx={{ mb: 2 }}
        helperText="Sin extensión .csv"
      />

      <FormControl component="fieldset" sx={{ mb: 2 }}>
        <FormLabel component="legend">Delimitador</FormLabel>
        <RadioGroup
          row
          value={delimiter}
          onChange={(e) => setDelimiter(e.target.value)}
        >
          <FormControlLabel value="," control={<Radio size="small" />} label="Coma (,)" />
          <FormControlLabel value=";" control={<Radio size="small" />} label="Punto y coma (;)" />
          <FormControlLabel value="\t" control={<Radio size="small" />} label="Tabulación" />
        </RadioGroup>
      </FormControl>

      <FormControl component="fieldset" sx={{ mb: 2 }}>
        <FormLabel component="legend">Incluir cabeceras</FormLabel>
        <RadioGroup
          row
          value={includeHeaders.toString()}
          onChange={(e) => setIncludeHeaders(e.target.value === 'true')}
        >
          <FormControlLabel value="true" control={<Radio size="small" />} label="Sí" />
          <FormControlLabel value="false" control={<Radio size="small" />} label="No" />
        </RadioGroup>
      </FormControl>

      <Divider sx={{ my: 2 }} />

      <Typography variant="body2" color="text.secondary" gutterBottom>
        Se exportarán {selectedColumns.length} columnas y {data.totalRows} filas
      </Typography>

      {selectedColumns.length === 0 ? (
        <Alert severity="warning" sx={{ mb: 2 }}>
          Selecciona al menos una columna para exportar
        </Alert>
      ) : (
        <Button
          variant="contained"
          fullWidth
          startIcon={<Download />}
          onClick={handleDownload}
          sx={{
            background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
            boxShadow: '0 3px 5px 2px rgba(33, 203, 243, .3)',
          }}
        >
          Descargar CSV
        </Button>
      )}
    </Box>
  )
}

export default ExportOptions