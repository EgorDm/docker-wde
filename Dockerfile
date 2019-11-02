FROM debian:stable-slim

# Constants
ENV DEV_USER magnetron
ENV DEV_HOME /home/${DEV_USER}
ENV DEV_DB_USER magnetron
ENV DEV_DB_PASS magnetron

# Install basics
RUN apt update && \
    apt install -y --no-install-recommends --no-upgrade sudo zip unzip iputils-ping curl wget dnsmasq less make && \
    apt install -y --no-install-recommends --no-upgrade vim git openssh-client openssh-server && \
# Install server parts
    apt install -y --no-install-recommends --no-upgrade nginx php openssl npm jq xsel libnss3-tools mariadb-server && \
    apt install -y --no-install-recommends --no-upgrade php-fpm php-curl php-gd php-intl php-imap php-mysql php-soap php-xmlrpc php-xsl php-pear php-xdebug && \
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
    valet domain dev && \
    valet park
VOLUME ["${DEV_HOME}/domains", "${DEV_HOME}/.valet"]

# Setup networking
RUN sudo sed -i s/\#user=/user=root/g /etc/dnsmasq.conf && \
    sudo sh -c "echo \"nameserver 127.0.0.1\nnameserver 1.1.1.1\" >| /etc/resolv.conf"

# Setup Database
RUN sudo service mysql start && \
    echo "CREATE USER '$DEV_DB_USER'@'localhost' IDENTIFIED BY '$DEV_DB_PASS'; \
          GRANT ALL PRIVILEGES ON * . * TO '$DEV_DB_USER'@'localhost'; \
          UPDATE mysql.user SET host = '%'" | sudo mysql -u root
RUN sudo service mysql stop && \
    sudo sed -e 's/^bind-address.*$/bind-address = 0.0.0.0/' -i /etc/mysql/mariadb.conf.d/50-server.cnf
VOLUME ["/var/lib/mysql", "/var/log/mysql", "/etc/mysql"]

# Startup services
ENTRYPOINT sudo service nginx start && \
    sudo service dnsmasq start && \
    sudo service php7.3-fpm start && \
    sudo service mysql start && \
    valet start

# Expose the ports
EXPOSE 80/tcp
EXPOSE 80/udp
EXPOSE 3306/tcp
EXPOSE 9000/tcp
