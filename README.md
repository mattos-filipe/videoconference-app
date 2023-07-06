# Integrantes do grupo
Alexandre dos Santos Gualberto 790843

Cauê Bonfim Trevisan
Kenzo Inanami de Faria 790778
Luiz Filipe de Almeida Mattos 772155



# Aplicativo de video-conferência
Criação de um aplicativo de videoconferência utilizando as bibliotecas ZeroMQ, openCV e pyaudio para a disciplina de sistemas distribuídos turma 2023/1 da UFSCar.

# Configuração do ambiente
Para rodar a aplicação é necessário ter a versão 3 do python e o gerenciador de pacotes pip instalados no computador. A instalação das bibliotecas será mostrada a seguir.

## Instalação do ZeroMQ
  O ZeroMQ foi a tecnologia empregada para fazer a comunicação entre os participantes da chamada. A arquitetura utilizada é a PUB/SUB
```bash
pip install pyzmq
```
## Instalação do OpenCV
  O OpenCV foi a tecnologia empregada para fazer tanto a captura da imagem da câmera, quanto a exibição das imagens recebidas.
```bash
pip install opencv-python
```


## Instalação da PyAudio
  A PyAudio foi a tecnologia empregada para fazer tanto a captura, quanto a reprodução dos áúdios recebidos.
```bash
pip install pyaudio
```
# Execução do programa
## Em computadores diferentes
  Depois de instaladas todas as bibliotecas, antes de executar, altere o código ./main.py e adicione a lista de ip's dos usuários no lugar indicado. Importante ressaltar que os usuários devem estar na mesma rede.

  Para descobrir o IPV4 em computadores windows, abra o terminal, execute o comando abaixo e pegue o IPV4:
  ```bash
ipconfig
  ```
  Em computadores Linux, utilize o comando
  ```bash
  hostname -I
  ```
  Então, basta executar o comando abaixo e substituir {id} por um número de 0 a 7 diferente dos participantes que já estão na chamada:
  ```bash
  python3 main.py {id}
  ```
## No mesmo computador
  Para iniciar a chamada no mesmo computador, deixe a lista de ip's do arquivo main.py como indicado.
  Basta, então, executar o comando abaixo e substituir {id} por um número de 0 a 7 diferente dos participantes que já estão na chamada:
  ```bash
  python3 main.py {id}
  ```
