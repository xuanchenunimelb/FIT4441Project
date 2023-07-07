// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Query
{
    bool private unverified;
    uint public remuneration;
    uint private c;
    address public client;
    address public node;
    uint8[] private op;
    uint32[] private id;
    uint8[] private v;
    bytes32[] private r;
    bytes32[] private s;

    bool private validity_;
    uint32[] private results_;

    constructor(uint counter) payable {
        require(msg.value > 0, "Remuneration must be greater than 0.");
        remuneration = msg.value;
        client = msg.sender;
        c = counter;
        unverified = true;
    }
    function upload_result(uint8[] memory ops, uint32[] memory ids,uint8[] memory vs, bytes32[] memory rs, bytes32[] memory ss) public{
        node = msg.sender;
        op = ops;
        id = ids;
        v = vs;
        r = rs;
        s = ss;
    }
    
    // function get_c() public view returns (string memory proofString, address recover_address) {
    //     bool validity = true;
    //     uint c_ = c;

    //     if (op.length != c_ || id.length != c_ || v.length != c_ || r.length != c_ || s.length != c_) {
    //         validity = false;
    //     }

    //     string memory proofString = string(abi.encodePacked("c=", toString(c_), "?op=", toString(op[0]), "?id=", toString(id[0])));
    //     bytes32 message = keccak256(abi.encodePacked(proofString));
    //     bytes32 prefixedHashMessage = keccak256(abi.encodePacked('\x19Ethereum Signed Message:\n32', message));
    //     // HashMessage = bytes32ToString(prefixedHashMessage);
    //     recover_address = ecr(prefixedHashMessage, v[0], r[0], s[0]);

    //     return (proofString, recover_address);
    // }
    function get_r() public view returns (bool v, uint32[] memory r){
        return(validity_, results_);
    }
    
    function verify() public returns (string[] memory strings, bool validity, uint32[] memory results, address[] memory recover_addresses, address node_) {
        require(unverified, "already verified");
        validity = true;
        uint c_ = c;
        uint32[] memory tempResults = new uint32[](c_);
        recover_addresses = new address[](c_);
        strings = new string[](c_);
        uint resultsCount = 0;

        if (op.length != c_ || id.length != c_ || v.length != c_ || r.length != c_ || s.length != c_) {
            validity = false;
        }

        for (uint i = 0; i < c_; i++) {
            string memory proofString = string(abi.encodePacked("c=", toString(i + 1), "?op=", toString(op[i]), "?id=", toString(id[i])));
            strings[i] = proofString;
            bool duplicate = false;
            // bytes32 message = keccak256(abi.encodePacked(proofString));
            bytes32 prefixedHashMessage = keccak256(abi.encodePacked('\x19Ethereum Signed Message:\n', uint2str(bytes(proofString).length), proofString));
            // HashMessage = bytes32ToString(prefixedHashMessage);
            address recover_address = ecr(prefixedHashMessage, v[i], r[i], s[i]);
            recover_addresses[i] = recover_address;
            if (recover_address != client) {
                validity = false;
            }else {
                if (op[i] == 1) {
                    duplicate = false;
                    for (uint k = 0; k < tempResults.length; k++) {
                        if (tempResults[k] == id[i]) {
                            // already exist
                            duplicate = true;
                        }
                    }
                    if(!duplicate){
                        tempResults[resultsCount] = id[i];
                        resultsCount++;
                    }
                } else if (op[i] == 0) {
                    // Find and remove the corresponding id from the results array
                    for (uint j = 0; j < tempResults.length; j++) {
                        if (tempResults[j] == id[i]) {
                            // Move the last element to the deleted position and reduce the length of the array
                            deleteElement(tempResults, j);
                            resultsCount--;
                            break;
                        }
                    }
                }
            }
            
        }
        results = new uint32[](resultsCount);

        for (uint i = 0; i < resultsCount; i++) {
            results[i] = tempResults[i];
        }

        // payable(node).transfer(address(this).balance);
        if(validity){
            payable(node).transfer(remuneration);
            // (bool sent, bytes memory data) = payable(node).call{value: address(this).balance}("");
            // require(sent, "Failed to send Ether");
        }else{
            payable(client).transfer(remuneration);
        }

        unverified = false;

        validity_ = validity;
        results_ = results;

        return (strings, validity, results, recover_addresses, node);
    }

    function transfereth() public {
        payable(node).transfer(address(this).balance);
    }

    function uint2str(uint _i) internal pure returns (string memory _uintAsString) {
        if (_i == 0) {
            return "0";
        }
        uint j = _i;
        uint len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint k = len;
        while (_i != 0) {
            k = k-1;
            uint8 temp = (48 + uint8(_i - _i / 10 * 10));
            bytes1 b1 = bytes1(temp);
            bstr[k] = b1;
            _i /= 10;
        }
        return string(bstr);
    }

    function deleteElement(uint32[] memory array, uint index) internal pure {
        if (index >= array.length) return;

        for (uint i = index; i < array.length - 1; i++) {
            array[i] = array[i + 1];
        }

        // Reduce the array length by 1
        assembly {
            mstore(array, sub(mload(array), 1))
        }
    }

    // function getMessageHash(string memory proofString) public pure returns(bytes32){
    //     return keccak256(abi.encodePacked(proofString));
    // }

    // function bytes32ToString(bytes32 hash) internal pure returns (string memory) {
    //     bytes memory buffer = new bytes(64);

    //     for (uint i = 0; i < 32; i++) {
    //         uint8 b = uint8(uint256(hash) >> (i * 8));
    //         uint8 hi = b >> 4;
    //         uint8 lo = b & 0x0f;

    //         buffer[i * 2] = char(hi);
    //         buffer[i * 2 + 1] = char(lo);
    //     }

    //     return string(buffer);
    // }

    // function char(uint8 b) internal pure returns (bytes1 c) {
    //     if (b < 10) {
    //         return bytes1(b + 48);
    //     } else {
    //         return bytes1(b + 87);
    //     }
    // }


    function ecr (bytes32 msgh, uint8 v_, bytes32 r_, bytes32 s_) public pure
    returns (address sender) {
      return ecrecover(msgh, v_, r_, s_);
    }

    function toString(uint256 value) internal pure returns (string memory) {
        if (value == 0) {
            return "0";
        }

        uint256 temp = value;
        uint256 digits;

        while (temp != 0) {
            digits++;
            temp /= 10;
        }

        bytes memory buffer = new bytes(digits);

        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }

        return string(buffer);
    }

    // function toString(bytes32 value) internal pure returns (string memory) {
    //     return string(abi.encodePacked(value));
    // }
    // function toString(bytes32 value) internal pure returns (string memory) {
    //     bytes memory buffer = new bytes(32);

    //     for (uint i = 0; i < 32; i++) {
    //         buffer[i] = value[i];
    //     }

    //     return string(buffer);
    // }
    
}