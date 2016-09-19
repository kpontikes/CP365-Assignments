import java.util.Random;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.HashSet;

class StackNode {

  public SlidingBoard board;
  public ArrayList<SlidingMove> path;

  public StackNode(SlidingBoard b, ArrayList<SlidingMove> p) {
    board = b;
    path = p;
  }
}


class IDSBot extends SlidingPlayer {

    ArrayList<SlidingMove> path;
    int move_number = -1;
    int MAX_DEPTH = 3;

    // The constructor gets the initial board
    public IDSBot(SlidingBoard _sb) {
        super(_sb);
        path = findPath(_sb, MAX_DEPTH);
    }

    // Based on in-class code for DFS
    public ArrayList<SlidingMove> findPath(SlidingBoard board, int max_depth) {
      HashSet<String> seen = new HashSet<String>();
      LinkedList<StackNode> stack = new LinkedList<StackNode>();
      StackNode currNode = new StackNode(board, new ArrayList<SlidingMove>());

      while (!currNode.board.isSolved()) {
        int depth = currNode.path.size();
        if(depth == max_depth){
          max_depth ++;
        }
        while (depth < max_depth) {
          ArrayList<SlidingMove> legal = currNode.board.getLegalMoves();
          for (SlidingMove move : legal) {
            SlidingBoard childBoard = new SlidingBoard(currNode.board.size);
            childBoard.setBoard(currNode.board);
            childBoard.doMove(move);
            if (!seen.contains(childBoard.toString())) {
              seen.add(childBoard.toString());
              ArrayList<SlidingMove> childPath = (ArrayList<SlidingMove>)currNode.path.clone();
              childPath.add(move);
              stack.add(new StackNode(childBoard, childPath));
            }
          // else {
          //   System.out.println("Already seen!");
          // }
        }
        }
        currNode = stack.pop();
      }
      return currNode.path;
    }

    // Perform a single move based on the current given board state
    public SlidingMove makeMove(SlidingBoard board) {
      move_number++;
      return path.get(move_number);
    }
}








//
