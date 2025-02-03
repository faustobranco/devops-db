def call(str_Build_id, str_image) {

  def obj_PodTemplate = """
        apiVersion: v1
        kind: Pod
        metadata:
          labels:
            some-label: "pod-template-${str_Build_id}"
        spec:
          containers:
          - name: container-1
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