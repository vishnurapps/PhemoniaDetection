FROM ubuntu:latest
WORKDIR /app
RUN apt update
RUN apt install -y python3 python3-pip
COPY . .
RUN pip3 install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install -r requirements.txt
EXPOSE 5011
CMD python3 basic.py
