#include <stdio.h> 

#include <fcntl.h> // Para open() 

#include <unistd.h> // Para read(), write(), close(), fork(), exec 

#include <sys/wait.h> // Para wait() 

 

#define BUFFER_SIZE 1024 

 

int main() { 

int file_descriptor; 

char buffer[BUFFER_SIZE]; 

ssize_t bytes_read; 

 

// 1. Abrir el archivo usando 'open' 

file_descriptor = open("archivo.txt", O_RDONLY); 

if (file_descriptor == -1) { 

perror("Error al abrir el archivo"); 

return 1; 

} 

 

// 2. Leer el contenido del archivo usando 'read' 

while ((bytes_read = read(file_descriptor, buffer, BUFFER_SIZE)) > 0) { 

// 3. Escribir el contenido leído a la salida estándar usando 'write' 

if (write(STDOUT_FILENO, buffer, bytes_read) == -1) { 

perror("Error al escribir en la salida estándar"); 

close(file_descriptor); // Cerrar el archivo en caso de error 

return 1; 

} 

} 

 

if (bytes_read == -1) { 

perror("Error al leer el archivo"); 

close(file_descriptor); 

return 1; 

} 

 

// 4. Crear un proceso hijo usando 'fork' 

pid_t pid = fork(); 

if (pid == -1) { 

perror("Error al crear el proceso hijo"); 

close(file_descriptor); 

return 1; 

} 

 

if (pid == 0) { 

// Proceso hijo 

printf("\nEste es el proceso hijo (PID: %d)\n", getpid()); 

 

 

 

// 5. Reemplazar el proceso hijo con 'exec' para ejecutar un comando 

execlp("ls", "ls", "-l", NULL); // Reemplaza el proceso hijo con 'ls -l' 

 

// Si execlp falla 

perror("Error al ejecutar exec"); 

return 1; 

} else { 

// Proceso padre 

printf("\nEste es el proceso padre (PID: %d), esperando al hijo.\n", getpid()); 

 

// Esperar a que el proceso hijo termine 

wait(NULL); 

 

// 6. Cerrar el archivo usando 'close' 

if (close(file_descriptor) == -1) { 

perror("Error al cerrar el archivo"); 

return 1; 

} 

 

printf("Archivo cerrado correctamente.\n"); 

} 

 

return 0; 

} 