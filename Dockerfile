FROM ubuntu:eoan

# Constants
ARG PHP_VERSION=7.3
ARG DEV_USER=magnetron
ENV DEV_HOME /home/${DEV_USER}

ENV DEBIAN_FRONTEND=noninteractive

# Install basics
RUN apt update && \
    apt install -yq --no-install-recommends --no-upgrade sudo zip unzip iputils-ping curl wget dnsmasq less make ca-certificates software-properties-common vim git openssh-client openssh-server && \
    add-apt-repository ppa:ondrej/php && \
# Install server parts
    apt install -yq --no-install-recommends --no-upgrade nginx php$PHP_VERSION openssl npm jq xsel libnss3-tools
RUN apt install -yq --no-install-recommends --no-upgrade php$PHP_VERSION-fpm php$PHP_VERSION-curl php$PHP_VERSION-gd php$PHP_VERSION-intl php$PHP_VERSION-imap php$PHP_VERSION-mysql php$PHP_VERSION-soap php$PHP_VERSION-xmlrpc php$PHP_VERSION-xsl php$PHP_VERSION-xml php$PHP_VERSION-xdebug php$PHP_VERSION-imagick imagemagick && \  
    apt install -y --no-install-recommends --no-upgrade composer

# Create a user
RUN useradd -ms /bin/bash ${DEV_USER} && \
    usermod -aG sudo ${DEV_USER} && \
    echo "${DEV_USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER ${DEV_USER}
WORKDIR ${DEV_HOME}

# Setup Valet
ENV PATH $DEV_HOME/.composer/vendor/bin:$PATH
RUN composer global require cpriego/valet-linux && \
    valet install && \
    mkdir $DEV_HOME/domains && \
    cd $DEV_HOME/domains && \
    valet domain DOMAIN_SUFFIX && \
    valet park
VOLUME ["${DEV_HOME}/domains", "${DEV_HOME}/.valet"]

# Setup networking
RUN sudo sed -i s/\#user=/user=root/g /etc/dnsmasq.conf && \
    sudo sh -c "echo \"nameserver 127.0.0.1\nnameserver 1.1.1.1\" >| /etc/resolv.conf"

# Startup services
CMD sudo service nginx start && \
    sudo service dnsmasq start && \
    sudo service php$PHP_VERSION-fpm start && \
    valet start && \
    tail -f /dev/null

# Expose the ports
EXPOSE 80/tcp
EXPOSE 80/udp
EXPOSE 9000/tcp
