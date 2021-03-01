# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    captured.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 12:16:25 by charles           #+#    #+#              #
#    Updated: 2021/03/01 17:33:44 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from typing import List, Optional


class Captured:
    def __init__(
        self,
        output: str,
        status: int,
        files_content: List[Optional[str]],
    ):
        """Captured class
           output:        captured content
           status:        command status
           files_content: content of the files altered by the command
        """

        self.output = output
        self.status = status
        self.files_content = files_content

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Captured):
            return False
        return (self.output == other.output and
                self.status == other.status and
                all(x == y for x, y in zip(self.files_content, other.files_content)))


class CapturedTimeout():
    pass
