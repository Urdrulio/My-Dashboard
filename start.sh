#!/bin/bash

# Script para iniciar la aplicación QVD to CSV Converter
echo "🚀 Iniciando QVD to CSV Converter..."

# Colores para el output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para verificar si un puerto está en uso
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js no está instalado. Por favor, instala Node.js primero.${NC}"
    exit 1
fi

# Verificar si las dependencias están instaladas
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Instalando dependencias...${NC}"
    npm install
fi

# Verificar puertos
if check_port 3001; then
    echo -e "${YELLOW}⚠️  El puerto 3001 ya está en uso. Cerrando proceso...${NC}"
    pkill -f "node server/index.js" 2>/dev/null || true
    sleep 2
fi

if check_port 3000; then
    echo -e "${YELLOW}⚠️  El puerto 3000 ya está en uso. Cerrando proceso...${NC}"
    pkill -f "vite" 2>/dev/null || true
    sleep 2
fi

# Crear directorio de uploads si no existe
if [ ! -d "uploads" ]; then
    mkdir uploads
    echo -e "${GREEN}📁 Directorio uploads creado${NC}"
fi

# Iniciar el servidor backend
echo -e "${BLUE}🔧 Iniciando servidor backend en puerto 3001...${NC}"
node server/index.js &
BACKEND_PID=$!

# Esperar un momento para que el backend se inicie
sleep 3

# Verificar si el backend se inició correctamente
if check_port 3001; then
    echo -e "${GREEN}✅ Servidor backend iniciado correctamente${NC}"
else
    echo -e "${RED}❌ Error al iniciar el servidor backend${NC}"
    exit 1
fi

# Iniciar el servidor frontend
echo -e "${BLUE}🎨 Iniciando servidor frontend en puerto 3000...${NC}"
npm run dev &
FRONTEND_PID=$!

# Esperar un momento para que el frontend se inicie
sleep 5

# Verificar si el frontend se inició correctamente
if check_port 3000; then
    echo -e "${GREEN}✅ Servidor frontend iniciado correctamente${NC}"
    echo ""
    echo -e "${GREEN}🎉 ¡Aplicación lista!${NC}"
    echo -e "${BLUE}🌐 Frontend: http://localhost:3000${NC}"
    echo -e "${BLUE}🔧 Backend:  http://localhost:3001${NC}"
    echo ""
    echo -e "${YELLOW}Para detener la aplicación, presiona Ctrl+C${NC}"
    echo ""
    
    # Intentar abrir el navegador automáticamente
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:3000 2>/dev/null
    elif command -v open &> /dev/null; then
        open http://localhost:3000 2>/dev/null
    fi
    
else
    echo -e "${RED}❌ Error al iniciar el servidor frontend${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Función para limpiar procesos al recibir señal de interrupción
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Deteniendo servidores...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    pkill -f "node server/index.js" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true
    echo -e "${GREEN}✅ Aplicación detenida${NC}"
    exit 0
}

# Capturar señales de interrupción
trap cleanup SIGINT SIGTERM

# Mantener el script ejecutándose
wait