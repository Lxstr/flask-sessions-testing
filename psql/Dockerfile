FROM postgres:14.4-alpine

COPY seed.sh /
RUN chown postgres /seed.sh \
    && chgrp postgres /seed.sh \
    && chmod 750 /seed.sh
CMD ["/bin/bash","-c","/seed.sh && tail -f /dev/null"]
