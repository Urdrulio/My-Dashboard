import React, { useState } from 'react'
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Paper,
  Grid,
} from '@mui/material'
import { Storage, Transform } from '@mui/icons-material'
import FileUploader from './components/FileUploader'
import DataPreview from './components/DataPreview'
import ColumnSelector from './components/ColumnSelector'
import ExportOptions from './components/ExportOptions'

interface QVDData {
  columns: string[]
  rows: Record<string, any>[]
  totalRows: number
}

function App() {
  const [qvdData, setQvdData] = useState<QVDData | null>(null)
  const [selectedColumns, setSelectedColumns] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleFileUpload = async (file: File) => {
    setIsLoading(true)
    try {
      // Aquí se implementará la lógica de subida y procesamiento del archivo QVD
      // Por ahora simulamos datos
      setTimeout(() => {
        const mockData: QVDData = {
          columns: [
            'LFAI_PKEY',
            'LFAI_BKEY',
            'LFAI_MANDT',
            'LFAI_LIFNR',
            'LFAI_LAND1',
            'LFAI_NAME1',
            'LFAI_NAME2',
            'LFAI_NAME3',
            'LFAI_NAME4',
            'LFAI_ORT01'
          ],
          rows: [
            {
              LFAI_PKEY: '100_1',
              LFAI_BKEY: 'Avid Factory (1)',
              LFAI_MANDT: '100',
              LFAI_LIFNR: '1',
              LFAI_LAND1: 'ES',
              LFAI_NAME1: 'Avid Factory',
              LFAI_NAME2: '',
              LFAI_NAME3: '',
              LFAI_NAME4: '',
              LFAI_ORT01: 'Madrid'
            },
            {
              LFAI_PKEY: '100_102',
              LFAI_BKEY: 'AGROFLOR (102)',
              LFAI_MANDT: '100',
              LFAI_LIFNR: '102',
              LFAI_LAND1: 'AT',
              LFAI_NAME1: 'AGROFLOR',
              LFAI_NAME2: 'Kunststoffgeselsc...',
              LFAI_NAME3: '',
              LFAI_NAME4: '',
              LFAI_ORT01: 'Wolfurt'
            },
            {
              LFAI_PKEY: '100_103',
              LFAI_BKEY: 'AQUARIUS GRA...',
              LFAI_MANDT: '100',
              LFAI_LIFNR: '103',
              LFAI_LAND1: 'DE',
              LFAI_NAME1: 'AQUARIUS GRA...',
              LFAI_NAME2: 'MICHAEL RATEIKE',
              LFAI_NAME3: '',
              LFAI_NAME4: '',
              LFAI_ORT01: 'Hasbergen'
            },
            {
              LFAI_PKEY: '100_104',
              LFAI_BKEY: 'ARBURG MASCH...',
              LFAI_MANDT: '100',
              LFAI_LIFNR: '104',
              LFAI_LAND1: 'DE',
              LFAI_NAME1: 'ARBURG MASCH...',
              LFAI_NAME2: 'HEHL & SOHNE ...',
              LFAI_NAME3: '',
              LFAI_NAME4: '',
              LFAI_ORT01: 'LOSSBURG'
            },
            {
              LFAI_PKEY: '100_105',
              LFAI_BKEY: 'AMPLIVERSAL D...',
              LFAI_MANDT: '100',
              LFAI_LIFNR: '105',
              LFAI_LAND1: 'DE',
              LFAI_NAME1: 'AMPLIVERSAL D...',
              LFAI_NAME2: 'KD-NR. 256259',
              LFAI_NAME3: '',
              LFAI_NAME4: '',
              LFAI_ORT01: 'LANGEN'
            },
            {
              LFAI_PKEY: '100_106',
              LFAI_BKEY: 'APETITO (106)',
              LFAI_MANDT: '100',
              LFAI_LIFNR: '106',
              LFAI_LAND1: 'DE',
              LFAI_NAME1: 'APETITO',
              LFAI_NAME2: 'K. DUESTENBERG',
              LFAI_NAME3: '',
              LFAI_NAME4: '',
              LFAI_ORT01: 'RHEINE'
            },
            {
              LFAI_PKEY: '100_110',
              LFAI_BKEY: 'Buschpost GmbH ...',
              LFAI_MANDT: '100',
              LFAI_LIFNR: '110',
              LFAI_LAND1: 'DE',
              LFAI_NAME1: 'Buschpost GmbH ...',
              LFAI_NAME2: 'Magnetventile',
              LFAI_NAME3: '',
              LFAI_NAME4: '',
              LFAI_ORT01: 'Vlotho'
            }
          ],
          totalRows: 100
        }
        setQvdData(mockData)
        setSelectedColumns(mockData.columns)
        setIsLoading(false)
      }, 1500)
    } catch (error) {
      console.error('Error al procesar el archivo:', error)
      setIsLoading(false)
    }
  }

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <Storage sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Convertidor QVD a CSV
          </Typography>
          <Transform sx={{ ml: 2 }} />
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Grid container spacing={3}>
          {/* Panel de carga de archivo */}
          <Grid item xs={12} md={6} lg={4}>
            <Paper
              elevation={3}
              sx={{
                p: 3,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
              }}
            >
              <Typography variant="h6" gutterBottom>
                Seleccionar Archivo QVD
              </Typography>
              <FileUploader onFileUpload={handleFileUpload} isLoading={isLoading} />
            </Paper>
          </Grid>

          {/* Panel de selección de columnas */}
          {qvdData && (
            <Grid item xs={12} md={6} lg={4}>
              <Paper elevation={3} sx={{ p: 3, height: 'fit-content' }}>
                <Typography variant="h6" gutterBottom>
                  Seleccionar Columnas
                </Typography>
                <ColumnSelector
                  columns={qvdData.columns}
                  selectedColumns={selectedColumns}
                  onSelectionChange={setSelectedColumns}
                />
              </Paper>
            </Grid>
          )}

          {/* Panel de opciones de exportación */}
          {qvdData && (
            <Grid item xs={12} md={6} lg={4}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Opciones de Exportación
                </Typography>
                <ExportOptions
                  data={qvdData}
                  selectedColumns={selectedColumns}
                />
              </Paper>
            </Grid>
          )}

          {/* Vista previa de datos */}
          {qvdData && (
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Vista Previa de Datos
                </Typography>
                <DataPreview
                  data={qvdData}
                  selectedColumns={selectedColumns}
                />
              </Paper>
            </Grid>
          )}
        </Grid>
      </Container>
    </Box>
  )
}

export default App