#!/usr/bin/env bash
apt-get update
"UserData"       : { "Fn::Base64" : { "Fn::Join" : ["", [
             "#!/bin/bash -xe\n",
             "yum install -y aws-cfn-bootstrap\n",

             "# Install the files and packages from the metadata\n",
             "/opt/aws/bin/cfn-init -v ",
             "         --stack ", { "Ref" : "AWS::StackName" },
             "         --resource WebServerInstance ",
             "         --configsets Install ",
             "         --region ", { "Ref" : "AWS::Region" }, "\n"
		]]}}





          #!/bin/bash -xe
        - |
          sudo apt-get update && sudo apt-get upgrade
          # Install Java 8
          sudo apt-get install openjdk-8-jdk
          sudo adduser hadoop -d /home/hadoop/
          echo hadoop | passwd hadoop --stdin
          sudo su - hadoop
          cd /home/hadoop/
          wget http://apache.cs.utah.edu/hadoop/common/current/hadoop-3.1.2.tar.gz
          tar -xzf hadoop-3.1.2.tar.gz
          mv hadoop-3.1.2 hadoop



        'Fn::Join':
          - ''
          - - |
              #!/bin/bash -xe
            - |
              yum install -y aws-cfn-bootstrap
            - |
              # Install the files and packages from the metadata
            - '/opt/aws/bin/cfn-init -v '
            - '         --stack '
            - !Ref 'AWS::StackName'
            - '         --resource WebServerInstance '
            - '         --configsets Install '
            - '         --region '
            - !Ref 'AWS::Region'
            - |+