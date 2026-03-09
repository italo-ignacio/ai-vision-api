from ultralytics import YOLO


def main():
    model = YOLO("yolov8s.pt")

    model.train(
        data="data.yaml",
        epochs=500,  # Quantidade de épocas (quantas vezes o modelo vê todo o dataset)
        imgsz=768,  # Tamanho das imagens usadas no treino (maior = melhor para objetos pequenos)
        batch=32,  # Quantidade de imagens processadas por batch
        device=0,  # GPU utilizada (0 = primeira GPU, "cpu" para usar CPU)
        workers=8,  # Quantidade de threads para carregar dados
        lr0=0.005,  # Learning rate inicial (velocidade de aprendizado)
        lrf=0.01,  # Learning rate final após o scheduler
        weight_decay=0.0005,  # Penalidade para evitar overfitting
        cos_lr=True,  # Usa scheduler de learning rate com curva coseno (treino mais estável)
        hsv_h=0.015,  # Variação no matiz da cor (Hue augmentation)
        hsv_s=0.7,  # Variação de saturação da imagem
        hsv_v=0.4,  # Variação de brilho da imagem
        degrees=10,  # Rotação aleatória da imagem (em graus)
        translate=0.1,  # Translação da imagem (move objetos horizontal/vertical)
        scale=0.5,  # Zoom in/out aleatório
        shear=2,  # Distorção da imagem (inclinação)
        fliplr=0.5,  # Probabilidade de flip horizontal (espelhamento)
        mosaic=1.0,  # Mosaic augmentation (combina 4 imagens em uma)
        mixup=0.1,  # Mistura duas imagens com pesos diferentes
        cache=True,  # Carrega dataset em RAM para acelerar treinamento
        patience=100,  # Early stopping (para se não melhorar após X epochs)
    )


if __name__ == "__main__":
    main()
