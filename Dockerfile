FROM ubuntu:eoan

# Constants
ARG PHP_VERSION=7.3
ENV PHP_VERSION=$PHP_VERSION

ENV DEBIAN_FRONTEND=noninteractive

# Install basics
ENV apti='apt install -yq --no-install-recommends --no-upgrade'
ENV PHP_EXTENSIONS='fpm curl gd intl imap mysql soap xmlrpc xsl xml xdebug imagick mbstring'

RUN apt update && \
    $apti sudo zip unzip curl dnsmasq ca-certificates software-properties-common vim git openssh-client && \
    add-apt-repository ppa:ondrej/php && \
    $apti nginx php$PHP_VERSION mysql-client openssl npm jq xsel libnss3-tools imagemagick
RUN $apti $(echo $PHP_EXTENSIONS | sed "s/[^ ]* */php${PHP_VERSION}-&/g") && \  
    $apti composer

# Create a user
ARG DEV_USER=magnetron
ENV DEV_HOME=/home/${DEV_USER}
ENV DEV_TOOLS=${DEV_HOME}/tools

RUN useradd -ms /bin/bash ${DEV_USER} && \
    usermod -aG sudo ${DEV_USER} && \
    echo "${DEV_USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER ${DEV_USER}
WORKDIR ${DEV_HOME}

ADD container $DEV_TOOLS

# Setup Valet
ARG DOMAIN_SUFFIX=dev
ENV DOMAIN_SUFFIX=$DOMAIN_SUFFIX
ENV DOMAINS=$DEV_HOME/domains

ENV PATH $DEV_HOME/.composer/vendor/bin:$PATH
RUN composer global require cpriego/valet-linux && \
    valet install && \
    mkdir $DOMAINS && \
    cd $DOMAINS && \
    valet domain $DOMAIN_SUFFIX && \
    valet park
VOLUME ["${DEV_HOME}/domains", "${DEV_HOME}/.valet/Certificates", "${DEV_HOME}/.valet/Log", "${DEV_HOME}/.valet/Nginx"]
RUN sudo chown -R $DEV_USER:$DEV_USER ${DEV_HOME}/.valet

# Expose the ports
EXPOSE 80/tcp
EXPOSE 80/udp
EXPOSE 443/tcp
EXPOSE 443/udp
EXPOSE 9000/tcp

CMD bash $DEV_TOOLS/startup.sh && \
    sudo service nginx start && \
    sudo service php$PHP_VERSION-fpm start && \
    valet start && \
    tail -f /dev/null
