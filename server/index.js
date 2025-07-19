const express = require('express')
const cors = require('cors')
const multer = require('multer')
const path = require('path')
const fs = require('fs')

const app = express()
const PORT = process.env.PORT || 3001

// Middleware
app.use(cors())
app.use(express.json())

// Configuración de multer para la subida de archivos
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = 'uploads'
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir)
    }
    cb(null, uploadDir)
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname)
  }
})

const upload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {
    if (path.extname(file.originalname).toLowerCase() === '.qvd') {
      cb(null, true)
    } else {
      cb(new Error('Solo se permiten archivos .qvd'), false)
    }
  },
  limits: {
    fileSize: 100 * 1024 * 1024 // 100MB máximo
  }
})

// Endpoint para subir y procesar archivos QVD
app.post('/api/upload-qvd', upload.single('qvdFile'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No se proporcionó ningún archivo' })
    }

    const filePath = req.file.path
    
    // Aquí se implementaría la lógica real para leer archivos QVD
    // Por ahora, simulamos el procesamiento
    
    // En un entorno real, necesitarías una librería específica para leer QVD
    // como node-qvd o similar
    
    const mockData = {
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
        }
      ],
      totalRows: 2,
      fileName: req.file.originalname
    }

    // Limpiar archivo temporal después del procesamiento
    fs.unlinkSync(filePath)

    res.json({
      success: true,
      data: mockData
    })

  } catch (error) {
    console.error('Error procesando archivo QVD:', error)
    res.status(500).json({ 
      error: 'Error interno del servidor',
      message: error.message 
    })
  }
})

// Endpoint para generar y descargar CSV
app.post('/api/generate-csv', (req, res) => {
  try {
    const { data, selectedColumns, options } = req.body
    
    if (!data || !selectedColumns || selectedColumns.length === 0) {
      return res.status(400).json({ error: 'Datos insuficientes para generar CSV' })
    }

    const { delimiter = ',', includeHeaders = true, fileName = 'export' } = options || {}

    // Generar contenido CSV
    const headers = selectedColumns
    const rows = data.rows.map(row => 
      selectedColumns.map(col => {
        const value = row[col]
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

    // Configurar headers para descarga
    res.setHeader('Content-Type', 'text/csv')
    res.setHeader('Content-Disposition', `attachment; filename="${fileName}.csv"`)
    
    res.send(csvContent)

  } catch (error) {
    console.error('Error generando CSV:', error)
    res.status(500).json({ 
      error: 'Error generando CSV',
      message: error.message 
    })
  }
})

// Manejo de errores de multer
app.use((error, req, res, next) => {
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ error: 'El archivo es demasiado grande (máximo 100MB)' })
    }
  }
  
  if (error.message === 'Solo se permiten archivos .qvd') {
    return res.status(400).json({ error: error.message })
  }

  res.status(500).json({ error: 'Error interno del servidor' })
})

app.listen(PORT, () => {
  console.log(`Servidor ejecutándose en puerto ${PORT}`)
})