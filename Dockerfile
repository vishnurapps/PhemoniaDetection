FROM ubuntu:latest
WORKDIR /app
RUN apt update
RUN apt install -y python3 python3-pip vim wget
COPY . .
RUN pip3 install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN mkdir -p /root/.cache/torch/checkpoints/
RUN wget https://download.pytorch.org/models/fasterrcnn_resnet50_fpn_coco-258fb6c6.pth -o /root/.cache/torch/checkpoints/fasterrcnn_resnet50_fpn_coco-258fb6c6.pth
RUN pip3 install -r requirements.txt
RUN mkdir uploads
RUN mkdir data
RUN mkdir images
EXPOSE 5011
CMD python3 basic.py
