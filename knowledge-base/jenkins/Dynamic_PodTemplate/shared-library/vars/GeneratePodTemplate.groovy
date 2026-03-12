def call(str_Build_id, str_image) {

  def obj_PodTemplate = """
        apiVersion: v1
        kind: Pod
        metadata:
          labels:
            some-label: "pod-template-${str_Build_id}"
        spec:
          securityContext:
            fsGroup: 1000
          containers:
          - name: jnlp
            image: registry.devops-db.internal:5000/jenkins-inbound-agent:latest
            imagePullPolicy: Always
          - name: container-1
            securityContext:
              runAsUser: 1000
              fsGroup: 1000          
            image: "${str_image}"
            env:
            - name: CONTAINER_NAME
              value: "container-1"
            - name: ANSIBLE_HOST_KEY_CHECKING
              value: "False"
            volumeMounts:
            - name: shared-volume
              mountPath: /mnt
            command:
            - cat
            tty: true
          volumes:
          - name: shared-volume
            emptyDir: {}
"""
  return obj_PodTemplate
}