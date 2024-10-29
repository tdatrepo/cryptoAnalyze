function subarrays(array, length) {
    const result = [];
    function generateSubarrays(start, current) {
        if (current.length === length) {
            result.push(check(current.slice())); 
            return;
        }
        for (let i = start; i < array.length; i++) {
            current.push(array[i]);
            generateSubarrays(i + 1, current);
            current.pop();
        }
    }
    generateSubarrays(0, []);
    return result;
}