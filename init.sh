# creating bucket where the tf states will be stored
aws s3api create-bucket --bucket empatica-tf-states --acl private --create-bucket-configuration LocationConstraint=eu-central-1 --profile empatica

