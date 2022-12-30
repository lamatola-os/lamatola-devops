mem_amount_total_with_unit=$(podman system info | grep 'memTotal: ' | tr -d 'memTotal: ')

unit=$(echo ${mem_amount_total_with_unit} | sed 's/[0-9\.]*//g')

mem_amount_total=$(echo ${mem_amount_total_with_unit} | sed 's/[^0-9\.]*//g')

mem_percent_used=$(podman stats --no-stream --format '{{.MemPerc}}' | tr -d '%' | paste -s -d '+' - | bc)

mem_percent_used=${mem_percent_used:-0}

mem_amount_used=$(echo "scale=2; ${mem_amount_total} * ${mem_percent_used} / 100" | bc)

echo "Memory Amount Total: ${mem_amount_total}${unit}"
echo "Memory Amount Used: ${mem_amount_used}${unit}"
echo "Memory Percent Used: ${mem_percent_used}%"
