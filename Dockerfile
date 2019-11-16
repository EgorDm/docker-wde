FROM ubuntu:eoan

# Constants
ENV DEBIAN_FRONTEND=noninteractive
ENV DEV_TOOLS=${DEV_HOME}/tools

# Install basics
ENV apti='apt install -yq --no-install-recommends --no-upgrade'

RUN apt update && \
    $apti sudo zip unzip curl dnsmasq ca-certificates software-properties-common vim git openssh-client

# Install nodejs
ADD container/install_node.sh $DEV_TOOLS/install_node.sh
RUN bash $DEV_TOOLS/install_node.sh

# Install php
ARG PHP_VERSION=7.3
ENV PHP_VERSION=$PHP_VERSION
ENV PHP_EXTENSIONS='fpm curl gd intl imap mysql soap xmlrpc xsl xml xdebug imagick mbstring'
RUN apt update && \
    add-apt-repository ppa:ondrej/php && \
    $apti nginx php$PHP_VERSION mysql-client openssl jq xsel libnss3-tools imagemagick
RUN $apti $(echo $PHP_EXTENSIONS | sed "s/[^ ]* */php${PHP_VERSION}-&/g")
RUN curl -s https://getcomposer.org/installer | php && \
    mv composer.phar /usr/local/bin/composer

ADD container/setup_php.sh $DEV_TOOLS/setup_php.sh
RUN bash $DEV_TOOLS/setup_php.sh

## Expose the ports
EXPOSE 80/tcp
EXPOSE 80/udp
EXPOSE 443/tcp
EXPOSE 443/udp
EXPOSE 9000/tcp

# Create a user
ARG DEV_USER=magnetron
ENV DEV_HOME=/home/${DEV_USER}

RUN useradd -ms /bin/bash ${DEV_USER} && \
    usermod -aG sudo ${DEV_USER} && \
    echo "${DEV_USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER ${DEV_USER}
WORKDIR ${DEV_HOME}

# Setup Valet
ARG DOMAIN_SUFFIX=dev
ENV DOMAIN_SUFFIX=$DOMAIN_SUFFIX
ENV DOMAINS=$DEV_HOME/domains

ENV PATH $DEV_HOME/.composer/vendor/bin:$PATH
ADD container/install_valet.sh $DEV_TOOLS/install_valet.sh
RUN bash $DEV_TOOLS/install_valet.sh
VOLUME ["${DEV_HOME}/domains", "${DEV_HOME}/.valet/Certificates", "${DEV_HOME}/.valet/Log", "${DEV_HOME}/.valet/Nginx"]
RUN sudo chown -R $DEV_USER:$DEV_USER ${DEV_HOME}/.valet

# Setup bash
ADD container/tools.sh $DEV_TOOLS/tools.sh
RUN echo "source $DEV_TOOLS/tools.sh" >> ${DEV_HOME}/.bashrc

ADD container/startup.sh $DEV_TOOLS/startup.sh
CMD bash $DEV_TOOLS/startup.sh && \
    tail -f /dev/null
