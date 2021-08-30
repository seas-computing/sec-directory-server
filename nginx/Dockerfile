FROM nginx:1.17.4-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN adduser -D app && mkdir -p /home/app/web/app/static && mkdir /home/app/web/app/media && chown -R app:app /home/app/
