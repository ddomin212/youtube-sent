folder_name=$1
first_time=$2
kernel_name=youtube-$folder_name
echo $folder_name
if [ $first_time == "yes" ]; then
    kaggle datasets create -p static/generated/$folder_name/dataset
else
    kaggle datasets version -p static/generated/$folder_name/dataset -m '"new"'
fi

sleep 10

kaggle k push -p static/generated/$folder_name/kernel

kernel_status="running"
while [[ $kernel_status != "complete" ]]; do
    kernel_status=$(kaggle kernels status $kernel_name | grep -oP 'status "\K\w+')
    printf "Kernel status: $kernel_status"
    sleep 10
done

kaggle kernels output $kernel_name -p static/generated/$folder_name/output