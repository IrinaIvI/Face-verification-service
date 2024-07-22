FROM debian:bookworm

ENV TERM xterm

# Настройки темы https://github.com/romkatv/powerlevel10k
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY .p10k.zsh /root/
COPY .zshrc /root/
