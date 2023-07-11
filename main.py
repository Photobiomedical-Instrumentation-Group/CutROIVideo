
import cv2
import numpy as np
import os

def cortar_video_ROI_manual(video_original, video_ROI):
    # Variáveis globais para armazenar as coordenadas da região de interesse (ROI)
    pontos = []
    selecionando = False
    pausado = False

    # Função para definir a região de interesse (ROI)
    def definir_ROI(event, x, y, flags, param):
        nonlocal pontos, selecionando, pausado

        if event == cv2.EVENT_LBUTTONDOWN:
            pontos = [(x, y)]
            selecionando = True
            pausado = True

        elif event == cv2.EVENT_LBUTTONUP:
            pontos.append((x, y))
            selecionando = False
            cv2.rectangle(frame, pontos[0], pontos[1], (255, 0, 0), 2)
            cv2.imshow('Video', frame)

    # Carregar o vídeo
    video = cv2.VideoCapture(video_original)

    # Ler o primeiro frame do vídeo
    _, frame = video.read()

    # Obter a largura e altura do vídeo
    video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Criar uma janela para exibir o vídeo
    cv2.namedWindow('Video')
    cv2.setMouseCallback('Video', definir_ROI)

    # Loop principal
    while True:
        # Exibir o frame atual
        cv2.imshow('Video', frame)

        # Aguardar a tecla 'q' para sair do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Verificar se a tecla Enter foi pressionada para pausar ou retomar o vídeo
        if cv2.waitKey(1) == 13:  # 13 é o código ASCII para a tecla Enter
            if not pausado:
                pausado = True
                cv2.destroyAllWindows()
            else:
                pausado = False
                cv2.namedWindow('Video')
                cv2.setMouseCallback('Video', definir_ROI)

        # Ler o próximo frame do vídeo se não estiver pausado
        if not pausado:
            _, frame = video.read()

        # Verificar se a região de interesse foi selecionada
        if not selecionando and not pausado and len(pontos) >= 2:
            break

    # Verificar se a região de interesse foi selecionada
    if len(pontos) < 2:
        print('Erro: Nenhuma região de interesse foi selecionada.')
        return

    # Definir os pontos da região de interesse
    x1, y1 = pontos[0]
    x2, y2 = pontos[1]

    # Obter as dimensões da região de interesse
    roi_width = abs(x2 - x1)
    roi_height = abs(y2 - y1)

    # Criar um objeto VideoWriter para salvar o vídeo final
    fourcc  = cv2.VideoWriter_fourcc(*'WMV1')
    saida = cv2.VideoWriter(video_ROI, fourcc , 30.0, (roi_width, roi_height))

    # Voltar ao início do vídeo
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Loop para processar cada frame e salvar no vídeo final
    while True:
        # Ler o próximo frame do vídeo
        ret, frame = video.read()
        if not ret:
            break

        # Cortar o frame na região de interesse
        frame_cortado = frame[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]

        # Salvar o frame no vídeo final
        saida.write(frame_cortado)

        # Desenhar o retângulo na região de interesse
        cv2.rectangle(frame, pontos[0], pontos[1], (255, 0, 0), 2)

        # Exibir o frame cortado
        cv2.imshow('Video Cortado', frame_cortado)

        # Aguardar a tecla 'q' para sair do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    video.release()
    saida.release()
    cv2.destroyAllWindows()

    

video_original = 'Video.wmv'
nome_arquivo = os.path.basename(video_original)
video_ROI = f'ROI_{nome_arquivo}'
cortar_video_ROI_manual(video_original, video_ROI)
