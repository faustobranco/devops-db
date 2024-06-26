$TTL 2d

$ORIGIN lab.devops-db.com.

@                    IN      SOA    ns1.lab.devops-db.com. admin.devops-db.com. (
                                    2022122800      ; serial
                                    12h             ; refresh
                                    15m             ; retry
                                    3w              ; expire
                                    2h              ; minimum ttl
                                    )

                     IN      NS     ns1.lab.devops-db.com.
*                    IN      NS     1.1.1.1
@                    IN      NS     1.1.1.1
ns1                  IN      A      172.21.5.155

; -- add dns records below

gitlab               IN      A      172.21.5.153
registry             IN      A      172.21.5.75
jenkins              IN      A      172.21.5.154
